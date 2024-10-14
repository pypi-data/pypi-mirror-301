from re import I
import time
import os
import logging
import random
from .base import PostTrainingBase
from PIL import ImageFilter
from backdoormbti.utils.data import get_dataloader,MixMatchDataset,SelfPoisonDataset,PoisonLabelDataset,CleanDataset
from torch.cuda.amp import autocast
from torch.cuda.amp import GradScaler
from torch.utils.data import DataLoader
import lightning as L
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import lr_scheduler
import pandas as pd
import numpy as np
from backdoormbti.utils.loss import MixMatchLoss, SCELoss, SimCLRLoss
from tabulate import tabulate
from torchvision import transforms
from collections import OrderedDict

class SelfModel(nn.Module):
    def __init__(self, backbone, head="mlp", proj_dim=128):
        super(SelfModel, self).__init__()
        self.backbone = backbone
        self.head = head

        if head == "linear":
            self.proj_head = nn.Linear(self.backbone.feature_dim, proj_dim)
        elif head == "mlp":
            self.proj_head = nn.Sequential(
                nn.Linear(self.backbone.feature_dim, self.backbone.feature_dim),
                nn.BatchNorm1d(self.backbone.feature_dim),
                nn.ReLU(),
                nn.Linear(self.backbone.feature_dim, proj_dim),
            )
        else:
            raise ValueError("Invalid head {}".format(head))

    def forward(self, x):
        feature = self.proj_head(self.backbone(x))
        feature = F.normalize(feature, dim=1)

        return feature
class LinearModel(nn.Module):
    def __init__(self, backbone, feature_dim, num_classes):
        super(LinearModel, self).__init__()
        self.backbone = backbone
        self.linear = nn.Linear(feature_dim, num_classes)

    def forward(self, x):
        feature = self.backbone(x)
        out = self.linear(feature)

        return out

    def update_encoder(self, backbone):
        self.backbone = backbone

def get_criterion(criterion_config):
    if "cross_entropy" in criterion_config:
        criterion = nn.CrossEntropyLoss(**criterion_config["cross_entropy"])
    elif "simclr" in criterion_config:
        criterion = SimCLRLoss(**criterion_config["simclr"])
    elif "sce" in criterion_config:
        criterion = SCELoss(**criterion_config["sce"])
    elif "mixmatch" in criterion_config:
        criterion = MixMatchLoss(**criterion_config["mixmatch"])
    else:
        raise ValueError(
            "Criterion {} is not supported.".format(criterion_config)
        )

    return criterion

def get_optimizer(model, optimizer_config):
    if "Adam" in optimizer_config:
        optimizer = torch.optim.Adam(model.parameters(), **optimizer_config["Adam"])
    elif "SGD" in optimizer_config:
        optimizer = torch.optim.SGD(model.parameters(), **optimizer_config["SGD"])
    else:
        raise NotImplementedError(
            "Optimizer {} is not supported.".format(optimizer_config)
        )

    return optimizer


def get_scheduler(optimizer, lr_scheduler_config):
    if lr_scheduler_config is None:
        scheduler = None
    elif "multi_step" in lr_scheduler_config:
        scheduler = lr_scheduler.MultiStepLR(
            optimizer, **lr_scheduler_config["multi_step"]
        )
    elif "cosine_annealing" in lr_scheduler_config:
        scheduler = lr_scheduler.CosineAnnealingLR(
            optimizer, **lr_scheduler_config["cosine_annealing"]
        )
    else:
        raise ValueError(
            "Learning rate scheduler {} is not supported.".format(lr_scheduler_config)
        )

    return scheduler

def tabulate_step_meter(batch_idx, num_batches, num_intervals, meter_list, logger):
    """Tabulate current average value of meters every ``step_interval``.

    Args:
        batch_idx (int): The batch index in an epoch.
        num_batches (int): The number of batch in an epoch.
        num_intervals (int): The number of interval to tabulate.
        meter_list (list or tuple of AverageMeter): A list of meters.
        logger (logging.logger): The logger.
    """
    step_interval = int(num_batches / num_intervals)
    if batch_idx % step_interval == 0:
        step_meter = {"Iteration": ["{}/{}".format(batch_idx, num_batches)]}
        for m in meter_list:
            step_meter[m.name] = [m.batch_avg]
        table = tabulate(step_meter, headers="keys", tablefmt="github", floatfmt=".5f")
        if batch_idx == 0:
            table = table.split("\n")
            table = "\n".join([table[1]] + table)
        else:
            table = table.split("\n")[2]
        logger.info(table)


def tabulate_epoch_meter(elapsed_time, meter_list, logger):
    """Tabulate total average value of meters every epoch.

    Args:
        eplased_time (float): The elapsed time of a epoch.
        meter_list (list or tuple of AverageMeter): A list of meters.
        logger (logging.logger): The logger.
    """
    epoch_meter = {m.name: [m.total_avg] for m in meter_list}
    epoch_meter["time"] = [elapsed_time]
    table = tabulate(epoch_meter, headers="keys", tablefmt="github", floatfmt=".5f")
    table = table.split("\n")
    table = "\n".join([table[1]] + table)
    logger.info(table)


def result2csv(result, log_dir):
    for k in result.keys():
        file_path = os.path.join(log_dir, k + ".csv")
        if not os.path.exists(file_path):
            df = pd.DataFrame.from_records([result[k]])
            df.to_csv(file_path, index=False)
        else:
            with open(file_path) as f:
                df = pd.read_csv(f)
                df = df._append(result[k], ignore_index=True)
                df.to_csv(file_path, index=False)

def load_state(
    model, resume, ckpt_dir, gpu, logger, optimizer=None, scheduler=None, is_best=False
):
    """Load training state from checkpoint.

    Args:
        model (torch.nn.Module): Model to resume.
        resume (string): Checkpoint name (empty string means the latest checkpoint)
            or False (means training from scratch).
        ckpt_dir (string): Checkpoint directory.
        gpu (string or int): The specified single gpu to load checkpoint.
        logger (logging.logger): The logger.
        optimizer (torch.optim.Optimizer): Optimizer to resume (default: None).
        scheduler (torch.optim._LRScheduler): Learning rate scheduler to
            resume (default: None).
        is_best (boolean, optional): Set True to load checkpoint
            with `best_acc` (default: False).

    Returns:
        resumed_epoch: The epoch to resume (0 means training from scratch.)
        best_acc: The best test accuracy in the training.
        best_epoch: The epoch getting the `best_acc`.
    """
    if resume == "False":
        logger.warning("Training from scratch.")
        resumed_epoch = 0
        if is_best:
            best_acc = 0
            best_epoch = 0
            return resumed_epoch, best_acc, best_epoch
        else:
            return resumed_epoch
    else:
        # Load checkpoint.
        if resume == "":
            ckpt_path = os.path.join(ckpt_dir, "latest_model.pt")
        else:
            ckpt_path = os.path.join(ckpt_dir, resume)
        ckpt = torch.load(ckpt_path, map_location="cuda:{}".format(gpu))
        logger.info("Load training state from the checkpoint {}:".format(ckpt_path))
        logger.info("Epoch: {}, result: {}".format(ckpt["epoch"], ckpt["result"]))
        if "parallel" in str(type(model)):
            # DataParallel or DistributedParallel.
            model.load_state_dict(ckpt["model_state_dict"])
        else:
            # Remove "module." in `model_state_dict` if saved
            # from DDP wrapped model in the single GPU training.
            model_state_dict = OrderedDict()
            for k, v in ckpt["model_state_dict"].items():
                if k.startswith("module."):
                    k = k.replace("module.", "")
                    model_state_dict[k] = v
                else:
                    model_state_dict[k] = v
            model.load_state_dict(model_state_dict)
        resumed_epoch = ckpt["epoch"]
        if optimizer is not None:
            optimizer.load_state_dict(ckpt["optimizer_state_dict"])
        if scheduler is not None:
            scheduler.load_state_dict(ckpt["scheduler_state_dict"])
        if is_best:
            best_acc = ckpt["best_acc"]
            best_epoch = ckpt["best_epoch"]
            return resumed_epoch, best_acc, best_epoch
        else:
            return resumed_epoch

class AverageMeter(object):
    """Computes and stores the average and current value.
    
    Modified from https://github.com/pytorch/examples/blob/master/imagenet/main.py
    """

    def __init__(self, name, fmt=None):
        self.name = name
        self.reset()

    def reset(self):
        self.batch_avg = 0
        self.total_avg = 0
        self.sum = 0
        self.count = 0

    def update(self, avg, n=1):
        self.batch_avg = avg
        self.sum += avg * n
        self.count += n
        self.total_avg = self.sum / self.count


class Record(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.reset()

    def reset(self):
        self.ptr = 0
        self.data = torch.zeros(self.size)

    def update(self, batch_data):
        self.data[self.ptr : self.ptr + len(batch_data)] = batch_data
        self.ptr += len(batch_data)

def get_saved_epoch(
    num_epochs, num_stage_epochs=100, min_interval=20, max_interval=100
):
    if num_epochs >= num_stage_epochs:
        early = set(range(min_interval, num_stage_epochs, min_interval))
        mid = set(range(num_stage_epochs, num_epochs - num_stage_epochs, max_interval))
        later = set(
            range(
                num_epochs - num_stage_epochs, num_epochs + min_interval, min_interval
            )
        )
        if num_epochs == num_stage_epochs:
            later.remove(0)
        saved_epoch = early.union(mid).union(later)
    else:
        raise ValueError(
            "The num_epochs: {} must be equal or greater than num_stage_epochs: {}".format(
                num_epochs, num_stage_epochs
            )
        )

    return saved_epoch

def simclr_train(model, loader, criterion, optimizer, logger, amp=False):
    loss_meter = AverageMeter("loss")
    meter_list = [loss_meter]

    model.train()
    # gpu = next(model.parameters()).device
    # ddp = isinstance(model, DistributedDataParallel)
    if amp:
        scaler = GradScaler()
    else:
        scaler = None
    start_time = time.time()
    for batch_idx, batch in enumerate(loader):
        img1, img2 = batch["img1"], batch["img2"]
        data = torch.cat([img1.unsqueeze(1), img2.unsqueeze(1)], dim=1)
        b, c, h, w = img1.size()
        data = data.view(-1, c, h, w)
        data = data.cuda(non_blocking=True)

        optimizer.zero_grad()
        if amp:
            with autocast():
                output = model(data).view(b, 2, -1)
                # if ddp:
                #     output = torch.cat(GatherLayer.apply(output), dim=0)
                loss = criterion(output)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            output = model(data).view(b, 2, -1)
            # if ddp:
            #     output = torch.cat(GatherLayer.apply(output), dim=0)
            loss = criterion(output)
            loss.backward()
            optimizer.step()

        loss_meter.update(loss.item())

        tabulate_step_meter(batch_idx, len(loader), 3, meter_list, logger)

    logger.info("Training summary:")
    tabulate_epoch_meter(time.time() - start_time, meter_list, logger)
    result = {m.name: m.total_avg for m in meter_list}

    return result

def poison_linear_train(model, loader, criterion, optimizer, logger, frozen=True):
    loss_meter = AverageMeter("loss")
    poison_loss_meter = AverageMeter("poison loss")
    clean_loss_meter = AverageMeter("clean loss")
    acc_meter = AverageMeter("acc")
    poison_acc_meter = AverageMeter("poison acc")
    clean_acc_meter = AverageMeter("clean acc")
    meter_list = [
        loss_meter,
        poison_loss_meter,
        clean_loss_meter,
        acc_meter,
        poison_acc_meter,
        clean_acc_meter,
    ]

    if frozen:
        # Freeze the backbone.
        for param in model.backbone.parameters():
            param.require_grad = False
    model.train()
    gpu = next(model.parameters()).device
    start_time = time.time()
    for batch_idx, batch in enumerate(loader):
        data = batch["img"].cuda(gpu, non_blocking=True)
        target = batch["target"].cuda(gpu, non_blocking=True)
        if frozen:
            with torch.no_grad():
                feature = model.backbone(data)
        else:
            feature = model.backbone(data)
        output = model.linear(feature)
        criterion.reduction = "none"
        raw_loss = criterion(output, target)
        criterion.reduction = "mean"
        loss = criterion(output, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        loss_meter.update(loss.item())
        pred = output.argmax(dim=1, keepdim=True)
        truth = pred.view_as(target).eq(target)
        acc_meter.update((torch.sum(truth).float() / len(truth)).item())
        poison_idx = torch.nonzero(batch["poison"], as_tuple=True)
        clean_idx = torch.nonzero(batch["poison"] - 1, as_tuple=True)
        # Not every batch contains poison data.
        if len(poison_idx[0]) != 0:
            poison_loss_meter.update(torch.mean(raw_loss[poison_idx]).item())
            poison_acc_meter.update(
                (torch.sum(truth[poison_idx]).float() / len(truth[poison_idx])).item()
            )
        clean_loss_meter.update(torch.mean(raw_loss[clean_idx]).item())
        clean_acc_meter.update(
            (torch.sum(truth[clean_idx]).float() / len(truth[clean_idx])).item()
        )

        tabulate_step_meter(batch_idx, len(loader), 3, meter_list, logger)

    if frozen:
        # Unfreeze the backbone.
        for param in model.backbone.parameters():
            param.require_grad = True
    logger.info("Linear training summary:")
    tabulate_epoch_meter(time.time() - start_time, meter_list, logger)
    result = {m.name: m.total_avg for m in meter_list}

    return result


def poison_linear_record(model, loader, criterion):
    num_data = len(loader.dataset)
    target_record = Record("target", num_data)
    poison_record = Record("poison", num_data)
    origin_record = Record("origin", num_data)
    loss_record = Record("loss", num_data)
    feature_record = Record("feature", (num_data, model.backbone.feature_dim))
    record_list = [
        target_record,
        poison_record,
        origin_record,
        loss_record,
        feature_record,
    ]

    model.eval()
    gpu = next(model.parameters()).device
    for _, batch in enumerate(loader):
        data = batch["img"].cuda(gpu, non_blocking=True)
        target = batch["target"].cuda(gpu, non_blocking=True)
        with torch.no_grad():
            feature = model.backbone(data)
            output = model.linear(feature)
        criterion.reduction = "none"
        raw_loss = criterion(output, target)

        target_record.update(batch["target"])
        poison_record.update(batch["poison"])
        origin_record.update(batch["origin"])
        loss_record.update(raw_loss.cpu())
        feature_record.update(feature.cpu())

    return record_list

def interleave_offsets(batch, nu):
    groups = [batch // (nu + 1)] * (nu + 1)
    for x in range(batch - sum(groups)):
        groups[-x - 1] += 1
    offsets = [0]
    for g in groups:
        offsets.append(offsets[-1] + g)
    assert offsets[-1] == batch

    return offsets

def interleave(xy, batch):
    nu = len(xy) - 1
    offsets = interleave_offsets(batch, nu)
    xy = [[v[offsets[p] : offsets[p + 1]] for p in range(nu + 1)] for v in xy]
    for i in range(1, nu + 1):
        xy[0][i], xy[i][i] = xy[i][i], xy[0][i]

    return [torch.cat(v, dim=0) for v in xy]

def mixmatch_train(
    model, xloader, uloader, criterion, optimizer, epoch, logger, **kwargs,
):
    loss_meter = AverageMeter("loss")
    xloss_meter = AverageMeter("xloss")
    uloss_meter = AverageMeter("uloss")
    lambda_u_meter = AverageMeter("lambda_u")
    meter_list = [loss_meter, xloss_meter, uloss_meter, lambda_u_meter]

    xiter = iter(xloader)
    uiter = iter(uloader)

    model.train()
    gpu = next(model.parameters()).device
    start = time.time()
    for batch_idx in range(kwargs["train_iteration"]):
        try:
            xbatch = next(xiter)
            xinput, xtarget = xbatch["img"], xbatch["target"]
        except:
            xiter = iter(xloader)
            xbatch = next(xiter)
            xinput, xtarget = xbatch["img"], xbatch["target"]

        try:
            ubatch = next(uiter)
            uinput1, uinput2 = ubatch["img1"], ubatch["img2"]
        except:
            uiter = iter(uloader)
            ubatch = next(uiter)
            uinput1, uinput2 = ubatch["img1"], ubatch["img2"]

        batch_size = xinput.size(0)
        xtarget = torch.zeros(batch_size, kwargs["num_classes"]).scatter_(
            1, xtarget.view(-1, 1).long(), 1
        )
        xinput = xinput.cuda(gpu, non_blocking=True)
        xtarget = xtarget.cuda(gpu, non_blocking=True)
        uinput1 = uinput1.cuda(gpu, non_blocking=True)
        uinput2 = uinput2.cuda(gpu, non_blocking=True)

        with torch.no_grad():
            # compute guessed labels of unlabel samples
            uoutput1 = model(uinput1)
            uoutput2 = model(uinput2)
            p = (torch.softmax(uoutput1, dim=1) + torch.softmax(uoutput2, dim=1)) / 2
            pt = p ** (1 / kwargs["temperature"])
            utarget = pt / pt.sum(dim=1, keepdim=True)
            utarget = utarget.detach()

        # mixup
        all_input = torch.cat([xinput, uinput1, uinput2], dim=0)
        all_target = torch.cat([xtarget, utarget, utarget], dim=0)
        l = np.random.beta(kwargs["alpha"], kwargs["alpha"])
        l = max(l, 1 - l)
        idx = torch.randperm(all_input.size(0))
        input_a, input_b = all_input, all_input[idx]
        target_a, target_b = all_target, all_target[idx]
        mixed_input = l * input_a + (1 - l) * input_b
        mixed_target = l * target_a + (1 - l) * target_b

        # interleave labeled and unlabeled samples between batches to get correct batchnorm calculation
        mixed_input = list(torch.split(mixed_input, batch_size))
        mixed_input = interleave(mixed_input, batch_size)

        logit = [model(mixed_input[0])]
        for input in mixed_input[1:]:
            logit.append(model(input))

        # put interleaved samples back
        logit = interleave(logit, batch_size)
        xlogit = logit[0]
        ulogit = torch.cat(logit[1:], dim=0)

        Lx, Lu, lambda_u = criterion(
            xlogit,
            mixed_target[:batch_size],
            ulogit,
            mixed_target[batch_size:],
            epoch + batch_idx / kwargs["train_iteration"],
        )
        loss = Lx + lambda_u * Lu
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        # ema_optimizer.step()

        loss_meter.update(loss.item())
        xloss_meter.update(Lx.item())
        uloss_meter.update(Lu.item())
        lambda_u_meter.update(lambda_u)
        tabulate_step_meter(batch_idx, kwargs["train_iteration"], 3, meter_list, logger)

    logger.info("MixMatch training summary:")
    tabulate_epoch_meter(time.time() - start, meter_list, logger)
    result = {m.name: m.total_avg for m in meter_list}

    return result


def get_semi_idx(record_list, ratio, logger):
    """Get labeled and unlabeled index.
    """
    keys = [r.name for r in record_list]
    loss = record_list[keys.index("loss")].data.numpy()
    poison = record_list[keys.index("poison")].data.numpy()
    semi_idx = np.zeros(len(loss))
    # Sort loss and fetch `ratio` of the smallest indices.
    indice = loss.argsort()[: int(len(loss) * ratio)]
    logger.info(
        "{}/{} poisoned samples in semi_idx".format(poison[indice].sum(), len(indice))
    )
    semi_idx[indice] = 1

    return semi_idx


def linear_test(model, loader, criterion, logger):
    loss_meter = AverageMeter("loss")
    acc_meter = AverageMeter("acc")
    meter_list = [loss_meter, acc_meter]

    model.eval()
    gpu = next(model.parameters()).device
    start_time = time.time()
    for batch_idx, batch in enumerate(loader):
        data = batch["img"].cuda(gpu, non_blocking=True)
        target = batch["target"].cuda(gpu, non_blocking=True)
        with torch.no_grad():
            output = model(data)
        criterion.reduction = "mean"
        loss = criterion(output, target)

        loss_meter.update(loss.item())
        pred = output.argmax(dim=1, keepdim=True)
        truth = pred.view_as(target).eq(target)
        acc_meter.update((torch.sum(truth).float() / len(truth)).item())

        tabulate_step_meter(batch_idx, len(loader), 2, meter_list, logger)

    logger.info("Linear test summary:")
    tabulate_epoch_meter(time.time() - start_time, meter_list, logger)
    result = {m.name: m.total_avg for m in meter_list}

    return result

class GaussianBlur(object):
    """Gaussian blur augmentation in SimCLR.
    
    Borrowed from https://github.com/facebookresearch/moco/blob/master/moco/loader.py.
    """

    def __init__(self, sigma=[0.1, 2.0]):
        self.sigma = sigma

    def __call__(self, x):
        sigma = random.uniform(self.sigma[0], self.sigma[1])
        x = x.filter(ImageFilter.GaussianBlur(radius=sigma))

        return x
    

class DBD(PostTrainingBase):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.logger = logging.getLogger("defense")
        self.stage = args.stage
        assert self.stage in ["simclr","mixmatch_finetune"] 
  
    def _setup_dataloaders(
        self,
        clean_train_set,
        clean_test_set,
        poison_train_set,
        poison_test_set,
        collate_fn,
        batch_size,
        num_workers,
        pin_memory):
        clean_train_loader = get_dataloader(
            dataset=clean_train_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=pin_memory,
        )
        clean_test_loader = get_dataloader(
            dataset=clean_test_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=pin_memory,
        )
        poison_test_loader = get_dataloader(
            dataset=poison_test_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=pin_memory,
        )
        poison_train_loader = get_dataloader(
            dataset=poison_train_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=pin_memory,
        )
        
        return clean_train_loader,clean_test_loader,poison_test_loader,poison_train_loader
    
    def setup(self,
        clean_train_set,
        clean_test_set,
        poison_train_set,
        poison_test_set,
        model,
        collate_fn,):
        # LightningModule，不如不用

        # 暂时放弃支持多卡，resnet18单卡足够

        self.backbone = model
        if self.stage == "simclr":
            self.clean_train_set = clean_train_set
            self.clean_test_set = clean_test_set
            self.poison_test_set = poison_test_set
            
            transform = transforms.Compose([
                transforms.RandomResizedCrop(size=32,scale=[0.2, 1.0],interpolation=3),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomApply([transforms.ColorJitter(brightness=0.4,contrast=0.4,saturation=0.4,hue=0.1)], p=0.5),
                transforms.RandomGrayscale(p=0.5),
                transforms.RandomApply([GaussianBlur(sigma=[0.1, 2.0])], p=0.5),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.2023, 0.1994, 0.2010])
            ])
            
            self.poison_train_set = SelfPoisonDataset(poison_train_set,transform)

            _ , _ , _ , self.poison_train_loader = self._setup_dataloaders(
                self.clean_train_set,
                self.clean_test_set,
                self.poison_train_set,
                self.poison_test_set,
                collate_fn,
                self.args.simclr["batch_size"],
                self.args.simclr["num_workers"],
                self.args.simclr["pin_memory"])
        
            self.self_model = SelfModel(backbone=self.backbone)
            self.self_model.cuda()
            self.logger.info("Create self model")

        elif self.stage == "mixmatch_finetune":
            self.self_model=SelfModel(self.backbone)
            load_state(
                self.self_model, self.args.mixmatch_finetune["pretrain_checkpoint"], self.args.mixmatch_finetune["pretrain_ckpt_dir"], 0, self.logger
            )
            self.linear_model = LinearModel(self.backbone, self.backbone.feature_dim, self.args.mixmatch_finetune["num_classes"])
            self.linear_model.cuda()
            self.clean_train_set = clean_train_set
            
            self.clean_test_set = CleanDataset(clean_test_set)

            transform = transforms.Compose([
                transforms.RandomCrop(size=32,padding=4,padding_mode="reflect"),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.2023, 0.1994, 0.2010])
            ])
            self.poison_train_set = PoisonLabelDataset(poison_train_set,transform)
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.2023, 0.1994, 0.2010])
            ]) 
            
            self.poison_test_set = PoisonLabelDataset(poison_test_set,transform)
            _ ,  self.clean_test_loader, self.poison_test_loader, self.poison_train_loader = self._setup_dataloaders(
                self.clean_train_set,
                self.clean_test_set,
                self.poison_train_set,
                self.poison_test_set,
                collate_fn,
                self.args.mixmatch_finetune["warmup"]["loader"]["batch_size"],
                self.args.mixmatch_finetune["warmup"]["loader"]["num_workers"],
                self.args.mixmatch_finetune["warmup"]["loader"]["pin_memory"])
                        
    def train_simclr(self):
        
        criterion = get_criterion(self.args.simclr["criterion"])
        self.logger.info("Create criterion: {}".format(criterion))
        optimizer = get_optimizer(self.self_model,self.args.simclr["optimizer"])
        self.logger.info("Create optimizer: {}".format(optimizer))
        scheduler = get_scheduler(optimizer,self.args.simclr["lr_scheduler"])
        self.logger.info("Create scheduler: {}".format(self.args.simclr["lr_scheduler"]))
        resumed_epoch = 0
        
        
        saved_epoch = get_saved_epoch(
            self.args.simclr["epochs"],
            self.args.simclr["num_stage_epochs"],
            self.args.simclr["min_interval"],
            self.args.simclr["max_interval"],
        )
        
        self.args.simclr["ckpt_dir"] = os.path.join(self.args.log_dir,"simclr/checkpoints")
        os.makedirs(self.args.simclr["ckpt_dir"],exist_ok=True)
        output = []
        for epoch in range(self.args.simclr["epochs"]-resumed_epoch):
            self.logger.info(
                "===Epoch: {}/{}===".format(epoch+ resumed_epoch+ 1, self.args.simclr["epochs"])
            )
            self.logger.info("SimCLR training...")
            self_train_result = simclr_train(
                self.self_model,self.poison_train_loader, criterion, optimizer, self.logger, self.args.simclr["amp"]
            )
            if scheduler is not None:       
                scheduler.step()
            output.append({
                "epoch":epoch,
                "result": self_train_result
            })
            result = {"self_train": self_train_result}
            result2csv(result, self.args.log_dir)
            saved_dict = {
                "epoch": epoch + resumed_epoch+ 1,
                "result": result,
                "model_state_dict": self.self_model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
            }
            if scheduler is not None:
                saved_dict["scheduler_state_dict"] = scheduler.state_dict()

            ckpt_path = os.path.join(self.args.simclr["ckpt_dir"], "latest_model.pt")
            torch.save(saved_dict, ckpt_path)
            self.logger.info("Save the latest model to {}".format(ckpt_path))
            if (epoch + resumed_epoch + 1) in saved_epoch:
                ckpt_path = os.path.join(
                    self.args.simclr["ckpt_dir"], "epoch{}.pt".format(epoch + resumed_epoch + 1)
                )
                torch.save(saved_dict, ckpt_path)
                self.logger.info("Save the model in saved epoch to {}".format(ckpt_path))                   

        return output
    
    # def train_supervise(self):
    #     criterion = get_criterion(self.args.supervise["criterion"])
    #     self.logger.info("Create criterion: {}".format(criterion))
    #     optimizer = get_optimizer(self.linear_model,self.args.supervise["optimizer"])
    #     self.logger.info("Create optimizer: {}".format(optimizer))
    #     scheduler = get_scheduler(optimizer,self.args.supervise["lr_scheduler"])
    #     self.logger.info("Create scheduler: {}".format(self.args.supervise["lr_scheduler"]))       
        
         
    #     pass
    
    def train_mixmatch_finetune(self):
        warmup_criterion = get_criterion(self.args.mixmatch_finetune["warmup"]["criterion"])
        self.logger.info("Create criterion: {} for warmup".format(warmup_criterion))
        warmup_criterion = warmup_criterion.cuda()
        semi_criterion = get_criterion(self.args.mixmatch_finetune["semi"]["criterion"])
        semi_criterion = semi_criterion.cuda()
        self.logger.info("Create criterion: {} for semi-training".format(semi_criterion))
        optimizer = get_optimizer(self.linear_model, self.args.mixmatch_finetune["optimizer"])
        self.logger.info("Create optimizer: {}".format(optimizer))
        scheduler = get_scheduler(optimizer, self.args.mixmatch_finetune["lr_scheduler"])
        self.logger.info("Create learning rete scheduler: {}".format(self.args.mixmatch_finetune["lr_scheduler"]))   

        self.args.mixmatch_finetune["ckpt_dir"] = os.path.join(self.args.log_dir,"mixmatch_finetune/checkpoints")
        os.makedirs(self.args.mixmatch_finetune["ckpt_dir"],exist_ok=True)
        num_epochs = self.args.mixmatch_finetune["warmup"]["num_epochs"] +  self.args.mixmatch_finetune["semi"]["num_epochs"]
        resumed_epoch = 0
        best_acc = 0
        for epoch in range(num_epochs - resumed_epoch):
            self.logger.info("===Epoch: {}/{}===".format(epoch + resumed_epoch + 1, num_epochs))
            if (epoch + resumed_epoch + 1) <=  self.args.mixmatch_finetune["warmup"]["num_epochs"]:
                self.logger.info("Poisoned linear warmup...")
                poison_train_result = poison_linear_train(
                    self.linear_model,
                    self.poison_train_loader,
                    warmup_criterion,
                    optimizer,
                    self.logger,
                )
            else:
                record_list = poison_linear_record(
                    self.linear_model, self.poison_test_loader, warmup_criterion
                )
                self.logger.info("Mining clean data from poisoned dataset...")
                semi_idx = get_semi_idx(record_list,  self.args.mixmatch_finetune["semi"]["epsilon"], self.logger)
                xdata = MixMatchDataset(self.poison_train_set, semi_idx, labeled=True)
                udata = MixMatchDataset(self.poison_train_set, semi_idx, labeled=False)
                xloader = DataLoader(
                    xdata,  **self.args.mixmatch_finetune["semi"]["loader"], shuffle=True, drop_last=True
                )
                uloader = DataLoader(
                    udata,  **self.args.mixmatch_finetune["semi"]["loader"], shuffle=True, drop_last=True
                )
                self.logger.info("MixMatch training...")
                poison_train_result = mixmatch_train(
                    self.linear_model,
                    xloader,
                    uloader,
                    semi_criterion,
                    optimizer,
                    epoch,
                    self.logger,
                    ** self.args.mixmatch_finetune["semi"]["mixmatch"]
                )
            self.logger.info("Test model on clean data...")
            clean_test_result = linear_test(
                self.linear_model, self.clean_test_loader, warmup_criterion, self.logger
            )
            self.logger.info("Test model on poison data...")
            poison_test_result = linear_test(
                self.linear_model, self.poison_test_loader, warmup_criterion, self.logger
            )
            if scheduler is not None:
                scheduler.step()
                self.logger.info(
                    "Adjust learning rate to {}".format(optimizer.param_groups[0]["lr"])
                )
            result = {
                "poison_train": poison_train_result,
                "poison_test": poison_test_result,
                "clean_test": clean_test_result,
            }
            result2csv(result, self.args.log_dir)

            is_best = False
            if clean_test_result["acc"] > best_acc:
                is_best = True
                best_acc = clean_test_result["acc"]
                best_epoch = epoch + resumed_epoch + 1
            self.logger.info("Best test accuaracy {} in epoch {}".format(best_acc, best_epoch))

            saved_dict = {
                "epoch": epoch + resumed_epoch + 1,
                "result": result,
                "model_state_dict": self.linear_model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "best_acc": best_acc,
                "best_epoch": best_epoch,
            }
            if scheduler is not None:
                saved_dict["scheduler_state_dict"] = scheduler.state_dict()

            if is_best:
                ckpt_path = os.path.join(self.args.mixmatch_finetune["ckpt_dir"], "best_model.pt")
                torch.save(saved_dict, ckpt_path)
                self.logger.info("Save the best model to {}".format(ckpt_path))
            ckpt_path = os.path.join(self.args.mixmatch_finetune["ckpt_dir"], "latest_model.pt")
            torch.save(saved_dict, ckpt_path)
            self.logger.info("Save the latest model to {}".format(ckpt_path))        
                
            pass
        
    def train(self):
        if self.stage == "simclr":
            self.train_simclr()
        # elif self.stage == "supervise":
        #     self.train_supervise()
        elif self.stage == "mixmatch_finetune":
            self.train_mixmatch_finetune()
        else:
            raise TypeError

    
    
    
    
    
    

        