from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
from backdoormbti.utils.eval import accuracy
from backdoormbti.defenses.base import DefenseBase
from backdoormbti.utils.train import retraining, testing
import copy
import logging
import random
import numpy as np
from backdoormbti.utils.data import get_dataloader
from backdoormbti.utils.optim import adjust_learning_rate
from torch.utils.data import Subset
from backdoormbti.configs.settings import DATA_DIR
from torchvision import transforms
from backdoormbti.utils.wrapper import get_data_spec_class_by_args

'''
AT with sum of absolute values with power p
code from: https://github.com/AberHu/Knowledge-Distillation-Zoo
'''
class AT(nn.Module):
	'''
	Paying More Attention to Attention: Improving the Performance of Convolutional
	Neural Netkworks wia Attention Transfer
	https://arxiv.org/pdf/1612.03928.pdf
	'''
	def __init__(self, p):
		super(AT, self).__init__()
		self.p = p

	def forward(self, fm_s, fm_t):
		loss = F.mse_loss(self.attention_map(fm_s), self.attention_map(fm_t))

		return loss

	def attention_map(self, fm, eps=1e-6):
		am = torch.pow(torch.abs(fm), self.p)
		am = torch.sum(am, dim=1, keepdim=True)
		norm = torch.norm(am, dim=(2,3), keepdim=True)
		am = torch.div(am, norm+eps)

		return am

class Cutout(object):
    """Randomly mask out one or more patches from an image.
    Args:
        n_holes (int): Number of patches to cut out of each image.
        length (int): The length (in pixels) of each square patch.
    """
    def __init__(self, n_holes, length):
        self.n_holes = n_holes
        self.length = length

    def __call__(self, img):
        """
        Args:
            img (Tensor): Tensor image of size (C, H, W).
        Returns:
            Tensor: Image with n_holes of dimension length x length cut out of it.
        """
        h = img.size(1)
        w = img.size(2)

        mask = np.ones((h, w), np.float32)

        for n in range(self.n_holes):
            y = np.random.randint(h)
            x = np.random.randint(w)

            y1 = np.clip(y - self.length // 2, 0, h)
            y2 = np.clip(y + self.length // 2, 0, h)
            x1 = np.clip(x - self.length // 2, 0, w)
            x2 = np.clip(x + self.length // 2, 0, w)

            mask[y1: y2, x1: x2] = 0.

        mask = torch.from_numpy(mask)
        mask = mask.expand_as(img)
        img = img * mask
        return img
	
class AverageMeter(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

"""
code from https://github.com/bboylyg/NAD
"""

class NAD(DefenseBase):
	def __init__(self, args) -> None:
		self.args = args
		
	def _train_step(self, tnet, sub_clean_train_loader, optimizer, criterions, epoch):
		for param in tnet.parameters():
			param.requires_grad = False

		at_losses = AverageMeter()
		top1 = AverageMeter()
		top5 = AverageMeter()
		

		criterionCls = criterions['criterionCls']
		criterionAT = criterions['criterionAT']

		self.model.train()

		for idx, (img, target, _, _) in enumerate(sub_clean_train_loader):
			if self.args.cuda:
				img = img.cuda()
				target = target.cuda()

			output_s, h1 = self.get_activations(self.model, img)
			output_t, h2= self.get_activations(tnet, img)
			# print(len(output_s))
			# remove hook
			

			at1_loss = 0.0
			cls_out = output_s[-1]
			cls_loss = criterionCls(cls_out, target)
			for activation_s, activation_t in zip(output_s[:-1], output_t[:-1]):
				# print(criterionAT(activation_s, activation_t.detach()))
				at1_loss += criterionAT(activation_s, activation_t.detach()) * self.args.beta
			# print(at1_loss.item(), cls_loss.item())
			at_loss = at1_loss + cls_loss

			prec1, prec5 = accuracy(cls_out, target, topk=(1, 5))
			at_losses.update(at_loss.item(), img.size(0))
			top1.update(prec1.item(), img.size(0))
			top5.update(prec5.item(), img.size(0))

			optimizer.zero_grad()
			at_loss.backward()
			optimizer.step()

			if idx % self.args.print_freq == 0:
				print('Epoch[{0}]:[{1:03}/{2:03}] '
					'AT_loss:{losses.val:.4f}({losses.avg:.4f}) '
					'prec@1:{top1.val:.2f}({top1.avg:.2f})  '
					'prec@5:{top5.val:.2f}({top5.avg:.2f})'.format(epoch, idx, len(sub_clean_train_loader), losses=at_losses, top1=top1, top5=top5))
			for handle in h1:
				handle.remove()
			for handle in h2:
				handle.remove()

	def _load_clean_dataset(self, transform=None, train=True):
		# label_idx = 1
		ds_dir = DATA_DIR / self.args.dataset
		match self.args.dataset.lower():
			# image dataset
			# case "mnist":
			#     from torchvision.datasets import MNIST

			#     dataset = MNIST(
			#         root=DATA_DIR / "MNIST",
			#         train=train,
			#         download=True,
			#         transform=transforms.ToTensor(),
			#     )
			case "cifar10":
				from torchvision.datasets import CIFAR10

				dataset = CIFAR10(
					root=ds_dir,
					train=train,
					download=True,
					transform=transform,
				)
			case "cifar100":
				from torchvision.datasets import CIFAR100
				dataset = CIFAR100(
					root=DATA_DIR / "CIFAR100",
					train=train,
					download=True,
					transform=transform,
				)
			case "gtsrb":
				from torchvision.datasets import GTSRB

				dataset = GTSRB(
					root=ds_dir,
					split="train" if train else "test",
					download=True,
					transform=transform,
				)
		DSW, MW, collate_fn = get_data_spec_class_by_args(self.args, "all")
		clean_train_set_wrapper = DSW(dataset)
		return clean_train_set_wrapper

	def get_sub_loader(self):
		train_num = int(len(self.clean_train_set) * self.args.ratio)
		# indices = [i for i in range(train_num)]
		transform = transforms.Compose([
        	transforms.RandomCrop(32, padding=4),
        	# transforms.RandomRotation(3),
        	transforms.RandomHorizontalFlip(),
        	transforms.ToTensor(),
        	Cutout(1, 3)
    	])

		clean_data = self._load_clean_dataset(transform)
		indices = random.sample(range(len(clean_data)), train_num)
		sub_clean_train_set = Subset(clean_data, indices)

		sub_clean_loader = get_dataloader(
            dataset= sub_clean_train_set,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=self.collate_fn,
            shuffle=True,
            pin_memory=True,
        )
		sub_clean_loader = self.fabric.setup_dataloaders(sub_clean_loader)
		return sub_clean_loader
	
	@staticmethod
	def get_activations(model, x_batch):
		outs, handles = [], []

		def layer_hook(module, input, output):
			outs.append(output.data)

		for layer in model.model.children():
			if isinstance(layer, nn.Sequential):
				handle = layer.register_forward_hook(layer_hook)
				handles.append(handle)
		pred = model.model(x_batch)
		outs.append(pred)
		return outs, handles

	
	def train(self):
		sub_clean_train_loader = self.get_sub_loader()
		
		tnet = copy.deepcopy(self.model)
		# print("------------------------test copy---------------------------")
		# result = testing(self.fabric, self.clean_test_loader, self.poison_test_loader, tnet, self.args)
		# print(result)
		# print(self.model.state_dict())
		# tnet.load_state_dict(self.model.state_dict())
		tnet, fine_tune_result = retraining(
            self.fabric,
            sub_clean_train_loader,
            self.clean_test_loader,
            self.poison_test_loader,
            tnet,
            self.args,
        )
		logger = logging.getLogger("defense")
		logger.info("fine tuning finished!")
		logger.info(fine_tune_result)
		# initialize optimizer
		optimizer = torch.optim.SGD(self.model.parameters(),
									lr=self.args.nad_lr,
									momentum=self.args.momentum,
									weight_decay=self.args.weight_decay,
									nesterov=True)

		# define loss functions
		if self.args.cuda:
			criterionCls = nn.CrossEntropyLoss().cuda()
			criterionAT = AT(self.args.p)
		else:
			criterionCls = nn.CrossEntropyLoss()
			criterionAT = AT(self.args.p)

		print('----------- NAD Train Initialization --------------')
		for epoch in range(0, self.args.epochs):

			# adjust_learning_rate(optimizer, epoch, self.args.nad_lr)

			# train every epoch
			criterions = {'criterionCls': criterionCls, 'criterionAT': criterionAT}

			if epoch == 0:
				# before training test firstly
				result = testing(self.fabric, self.clean_test_loader, self.poison_test_loader, self.model, self.args)	
				logger.info(result)

			self._train_step(tnet, sub_clean_train_loader, optimizer, criterions, epoch+1)

		# evaluate on testing set
		tnet.model.to(torch.device("cpu"))

		logger.info('NAD finish, testing the models......')
		result = testing(self.fabric, self.clean_test_loader, self.poison_test_loader, self.model, self.args)	
		logger.info(result)
			

