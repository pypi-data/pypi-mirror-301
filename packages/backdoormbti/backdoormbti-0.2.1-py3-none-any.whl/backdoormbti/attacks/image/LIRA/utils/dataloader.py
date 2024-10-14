from torchvision import datasets
from torchvision import transforms
from torch.utils import data
import torch.nn as nn


def get_transform(opt, train=True, pretensor_transform=False):
    transforms_list = []
    transforms_list.append(transforms.Resize((opt.input_height, opt.input_width)))
    if pretensor_transform:
        if train:
            transforms_list.append(transforms.RandomCrop((opt.input_height, opt.input_width), padding=opt.random_crop))
            transforms_list.append(transforms.RandomRotation(opt.random_rotation))
            if opt.dataset == "cifar10":
                transforms_list.append(transforms.RandomHorizontalFlip(p=0.5))

    transforms_list.append(transforms.ToTensor())
    if opt.dataset == "cifar10":
        transforms_list.append(transforms.Normalize([0.4914, 0.4822, 0.4465], [0.247, 0.243, 0.261]))
    else:
        raise Exception("Invalid Dataset")
    return transforms.Compose(transforms_list)


class PostTensorTransform(nn.Module):
    def __init__(self, opt):
        super(PostTensorTransform, self).__init__()
        self.random_crop = transforms.RandomCrop((opt.input_height, opt.input_width), padding=opt.random_crop)
        self.random_rotation = transforms.RandomRotation(opt.random_rotation)
        if opt.dataset == "cifar10":
            self.random_horizontal_flip = transforms.RandomHorizontalFlip(p=0.5)

    def forward(self, x):
        for module in self.children():
            x = module(x)
        return x



def get_dataloader(opt, train=True, pretensor_transform=False, min_width=0):
    transform = get_transform(opt, train, pretensor_transform)
    
    if opt.dataset == "cifar10":
        dataset = datasets.CIFAR10(
            root='./data', train=train, download=True, transform=transform)
    else:
        raise Exception("Invalid dataset")
    
    dataloader = data.DataLoader(
        dataset, batch_size=opt.batch_size, num_workers=opt.num_workers, shuffle=True)
    return dataloader
