"""
This file is modified based on the following source:
link : https://github.com/bboylyg/ABL.
The defense method is called abl.

The update include:
    1. data preprocess and dataset setting
    2. model setting
    3. args and config
    4. save process
    5. new standard: robust accuracy
basic sturcture for defense method:
    1. basic setting: args
    2. attack result(model, train data, test data)
    3. abl defense:
        a. pre-train model
        b. isolate the special data(loss is low) as backdoor data
        c. unlearn the backdoor data and learn the remaining data
    4. test the result and get ASR, ACC, RC
"""
import os
import sys

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from tqdm import tqdm

sys.path.append("../")
sys.path.append(os.getcwd())

import logging
import torchvision.transforms as transforms


class LGALoss(nn.Module):
    def __init__(self, gamma, criterion):
        super(LGALoss, self).__init__()
        self.gamma = gamma
        self.criterion = criterion
        return

    def forward(self, output, target):
        loss = self.criterion(output, target)
        # add Local Gradient Ascent(LGA) loss
        loss_ascent = torch.sign(loss - self.gamma) * loss
        return loss_ascent


class FloodingLoss(nn.Module):
    def __init__(self, flooding, criterion):
        super(FloodingLoss, self).__init__()
        self.flooding = flooding
        self.criterion = criterion
        return

    def forward(self, output, target):
        loss = self.criterion(output, target)
        # add Local Gradient Ascent(LGA) loss
        loss_ascent = (loss - self.flooding).abs() + self.flooding
        return loss_ascent


def adjust_learning_rate(optimizer, epoch, args):
    """set learning rate during the process of pretraining model
    optimizer:
        optimizer during the pretrain process
    epoch:
        current epoch
    args:
        Contains default parameters
    """
    if epoch < args.tuning_epochs:
        lr = args.lr
    else:
        lr = 0.01
    logging.info("epoch: {}  lr: {:.4f}".format(epoch, lr))
    for param_group in optimizer.param_groups:
        param_group["lr"] = lr


def compute_loss_value(args, poisoned_data, model_ascent):
    """Calculate loss value per example
    args:
        Contains default parameters
    poisoned_data:
        the train dataset which contains backdoor data
    model_ascent:
        the model after the process of pretrain
    """
    # Define loss function
    if args.device == "cuda":
        criterion = torch.nn.CrossEntropyLoss().cuda()
    else:
        criterion = torch.nn.CrossEntropyLoss()

    model_ascent.eval()
    losses_record = []

    example_data_loader = torch.utils.data.DataLoader(
        dataset=poisoned_data,
        batch_size=1,
        shuffle=False,
    )

    for idx, (img, target, _, _) in tqdm(enumerate(example_data_loader, start=0)):
        img = img.to(args.device)
        target = target.to(args.device)

        with torch.no_grad():
            output = model_ascent(img)
            loss = criterion(output, target)

        losses_record.append(loss.item())

    losses_idx = np.argsort(
        np.array(losses_record)
    )  # get the index of examples by loss value in descending order

    # Show the top 10 loss values
    losses_record_arr = np.array(losses_record)
    logging.info(f"Top ten loss value: {losses_record_arr[losses_idx[:10]]}")

    return losses_idx


def isolate_data(args, poison_data, losses_idx):
    """isolate the backdoor data with the calculated loss
    args:
        Contains default parameters
    result:
        the attack result contain the train dataset which contains backdoor data
    losses_idx:
        the index of order about the loss value for each data
    """
    # Initialize lists
    ratio = args.isolation_ratio
    perm = losses_idx[0 : int(len(losses_idx) * ratio)]
    permnot = losses_idx[int(len(losses_idx) * ratio) :]
    train_dataset = poison_data
    data_set_isolate = poison_data
    data_set_other = train_dataset
    data_set_isolate = Subset(data_set_isolate, perm)
    data_set_other = Subset(data_set_other, permnot)
    print("Finish collecting {} isolation examples: ".format(len(data_set_isolate)))
    print("Finish collecting {} other examples: ".format(len(data_set_other)))
    logging.info(
        "Finish collecting {} isolation examples: ".format(len(data_set_isolate))
    )
    logging.info("Finish collecting {} other examples: ".format(len(data_set_other)))

    return data_set_isolate, data_set_other


def learning_rate_finetuning(optimizer, epoch, args):
    """set learning rate during the process of finetuing model
    optimizer:
        optimizer during the pretrain process
    epoch:
        current epoch
    args:
        Contains default parameters
    """
    if epoch < 40:
        lr = 0.01
    elif epoch < 60:
        lr = 0.001
    else:
        lr = 0.001
    logging.info("epoch: {}  lr: {:.4f}".format(epoch, lr))
    for param_group in optimizer.param_groups:
        param_group["lr"] = lr


def learning_rate_unlearning(optimizer, epoch, args):
    """set learning rate during the process of unlearning model
    optimizer:
        optimizer during the pretrain process
    epoch:
        current epoch
    args:
        Contains default parameters
    """
    if epoch < args.unlearning_epochs:
        lr = 0.0001
    else:
        lr = 0.0001
    logging.info("epoch: {}  lr: {:.4f}".format(epoch, lr))
    for param_group in optimizer.param_groups:
        param_group["lr"] = lr


class ABL:
    def __init__(self, clean_train_loader, clean_test_loader, model, args) -> None:
        self.clean_train_loader = clean_train_loader
        self.clean_test_loader = clean_test_loader
        self.model = model.model
        self.ImageWappermodel = model
        self.args = args

    def repair(self, poison_test_set, poison_train_set):
        poison_train_loader = DataLoader(
            dataset=poison_train_set,
            batch_size=self.args.batch_size,
            drop_last=True,
            collate_fn=self.args.collate_fn,
            num_workers=self.args.num_workers,
            persistent_workers=True,
            pin_memory=True,
        )
        poison_test_loader = DataLoader(
            dataset=poison_test_set,
            batch_size=self.args.batch_size,
            drop_last=True,
            collate_fn=self.args.collate_fn,
            num_workers=self.args.num_workers,
            persistent_workers=True,
            pin_memory=True,
        )
        ###a. pre-train model
        poisoned_data, model_ascent = self.pre_train(
            self.args,
            poison_train_loader,
            poison_test_loader,
            self.clean_train_loader,
            self.clean_test_loader,
        )
        ###b. isolate the special data(loss is low) as backdoor data
        losses_idx = compute_loss_value(self.args, poisoned_data, model_ascent)
        logging.info("----------- Collect isolation data -----------")
        isolation_examples, other_examples = isolate_data(
            self.args, poisoned_data, losses_idx
        )

        ###c. unlearn the backdoor data and learn the remaining data
        model_new = self.train_unlearning(
            self.args,
            self.clean_test_loader,
            poison_test_loader,
            model_ascent,
            isolation_examples,
            other_examples,
        )
        return 1

    def pre_train(
        self,
        args,
        poison_train_loader,
        poison_test_loader,
        clean_train_loader,
        clean_test_loader,
    ):
        """Pretrain the model with raw data
        args:
            Contains default parameters
        result:
            attack result(details can be found in utils)
        """
        # Load models
        logging.info("----------- Network Initialization --------------")
        from torchvision.models import resnet18

        model_ascent = resnet18(num_classes=args.num_classes).to(self.args.device)
        logging.info("finished model init...")
        # initialize optimizer
        # because the optimizer has parameter nesterov
        optimizer = torch.optim.SGD(
            model_ascent.parameters(),
            lr=args.lr,
            momentum=args.momentum,
            weight_decay=args.weight_decay,
            nesterov=True,
        )

        # define loss functions
        # recommend to use cross entropy
        criterion = nn.CrossEntropyLoss().to(self.args.device)
        if args.gradient_ascent_type == "LGA":
            criterion = LGALoss(args.gamma, criterion).to(args.device)
        elif args.gradient_ascent_type == "Flooding":
            criterion = FloodingLoss(args.flooding, criterion).to(args.device)
        else:
            raise NotImplementedError
        logging.info("----------- Data Initialization --------------")
        logging.info("----------- Train Initialization --------------")
        for epoch in range(0, args.tuning_epochs):
            logging.info("Epoch {}:".format(epoch + 1))
            adjust_learning_rate(optimizer, epoch, args)
            (
                train_epoch_loss_avg_over_batch,
                train_mix_acc,
                train_clean_acc,
                train_asr,
                train_ra,
            ) = self.train_step(
                args, poison_train_loader, model_ascent, optimizer, criterion, epoch + 1
            )
            print(f"train_clean_acc:{train_clean_acc}")
            print(f"train_asr:{train_asr}")
            (
                clean_test_loss_avg_over_batch,
                bd_test_loss_avg_over_batch,
                ra_test_loss_avg_over_batch,
                test_acc,
                test_asr,
                test_ra,
            ) = self.eval_step(
                model_ascent,
                clean_test_loader,
                poison_test_loader,
                args,
            )
            print(f"test_acc:{test_acc}")
            print(f"test_asr:{test_asr}")
        return poison_train_loader.dataset, model_ascent

    def train_unlearning(
        self,
        args,
        clean_test_loader,
        poison_test_loader,
        model_ascent,
        isolate_poisoned_data,
        isolate_other_data,
    ):
        """train the model with remaining data and unlearn the backdoor data
        args:
            Contains default parameters
        result:
            attack result(details can be found in utils)
        model_ascent:
            the model after pretrain
        isolate_poisoned_data:
            the dataset of 'backdoor' data
        isolate_other_data:
            the dataset of remaining data
        """
        logging.info("Finish loading ascent model...")
        # initialize optimizer
        # Because nesterov we do not use other optimizer
        optimizer = torch.optim.SGD(
            model_ascent.parameters(),
            lr=args.lr,
            momentum=args.momentum,
            weight_decay=args.weight_decay,
            nesterov=True,
        )

        # define loss functions
        # you can use other criterion, but the paper use cross validation to unlearn sample
        criterion = nn.CrossEntropyLoss().to(self.args.device)
        isolate_poisoned_data_loader = torch.utils.data.DataLoader(
            dataset=isolate_poisoned_data,
            batch_size=args.batch_size,
            shuffle=True,
        )

        isolate_other_data_loader = torch.utils.data.DataLoader(
            dataset=isolate_other_data,
            batch_size=args.batch_size,
            shuffle=True,
        )

        data_bd_testset = poison_test_loader.dataset
        data_bd_loader = torch.utils.data.DataLoader(
            data_bd_testset,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            drop_last=False,
            shuffle=True,
            pin_memory=args.pin_memory,
        )

        data_clean_testset = clean_test_loader.dataset
        data_clean_loader = torch.utils.data.DataLoader(
            data_clean_testset,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            drop_last=False,
            shuffle=True,
            pin_memory=args.pin_memory,
        )

        train_loss_list = []
        train_mix_acc_list = []
        train_clean_acc_list = []
        train_asr_list = []
        train_ra_list = []

        clean_test_loss_list = []
        bd_test_loss_list = []
        ra_test_loss_list = []
        test_acc_list = []
        test_asr_list = []
        test_ra_list = []

        logging.info("----------- Train Initialization --------------")

        if args.finetuning_ascent_model == True:
            # this is to improve the clean accuracy of isolation model, you can skip this step
            logging.info("----------- Finetuning isolation model --------------")
            for epoch in range(0, args.finetuning_epochs):
                learning_rate_finetuning(optimizer, epoch, args)
                (
                    train_epoch_loss_avg_over_batch,
                    train_mix_acc,
                    train_clean_acc,
                    train_asr,
                    train_ra,
                ) = self.train_step(
                    args,
                    isolate_other_data_loader,
                    model_ascent,
                    optimizer,
                    criterion,
                    epoch + 1,
                )

                (
                    clean_test_loss_avg_over_batch,
                    bd_test_loss_avg_over_batch,
                    ra_test_loss_avg_over_batch,
                    test_acc,
                    test_asr,
                    test_ra,
                ) = self.eval_step(
                    model_ascent,
                    data_clean_loader,
                    data_bd_loader,
                    args,
                )

                train_loss_list.append(train_epoch_loss_avg_over_batch)
                train_mix_acc_list.append(train_mix_acc)
                train_clean_acc_list.append(train_clean_acc)
                train_asr_list.append(train_asr)
                train_ra_list.append(train_ra)

                clean_test_loss_list.append(clean_test_loss_avg_over_batch)
                bd_test_loss_list.append(bd_test_loss_avg_over_batch)
                ra_test_loss_list.append(ra_test_loss_avg_over_batch)
                test_acc_list.append(test_acc)
                test_asr_list.append(test_asr)
                test_ra_list.append(test_ra)

        logging.info("----------- Model unlearning --------------")
        for epoch in range(0, args.unlearning_epochs):
            learning_rate_unlearning(optimizer, epoch, args)
            (
                train_epoch_loss_avg_over_batch,
                train_mix_acc,
                train_clean_acc,
                train_asr,
                train_ra,
            ) = self.train_step_unlearn(
                args,
                isolate_poisoned_data_loader,
                model_ascent,
                optimizer,
                criterion,
                epoch + 1,
            )

            (
                clean_test_loss_avg_over_batch,
                bd_test_loss_avg_over_batch,
                ra_test_loss_avg_over_batch,
                test_acc,
                test_asr,
                test_ra,
            ) = self.eval_step(
                model_ascent,
                data_clean_loader,
                data_bd_loader,
                args,
            )

            train_loss_list.append(train_epoch_loss_avg_over_batch)
            train_mix_acc_list.append(train_mix_acc)
            train_clean_acc_list.append(train_clean_acc)
            train_asr_list.append(train_asr)
            train_ra_list.append(train_ra)

            clean_test_loss_list.append(clean_test_loss_avg_over_batch)
            bd_test_loss_list.append(bd_test_loss_avg_over_batch)
            ra_test_loss_list.append(ra_test_loss_avg_over_batch)
            test_acc_list.append(test_acc)
            test_asr_list.append(test_asr)
            test_ra_list.append(test_ra)
        print(f"test_acc_list:{test_acc_list}")
        print(f"test_asr_list:{test_asr_list}")
        return model_ascent

    def train_step(self, args, train_loader, model_ascent, optimizer, criterion, epoch):
        """Pretrain the model with raw data for each step
        args:
            Contains default parameters
        train_loader:
            the dataloader of train data
        model_ascent:
            the initial model
        optimizer:
            optimizer during the pretrain process
        criterion:
            criterion during the pretrain process
        epoch:
            current epoch
        """
        losses = 0
        size = 0

        batch_loss_list = []
        batch_predict_list = []
        batch_label_list = []
        batch_poison_indicator_list = []
        batch_original_targets_list = []
        model_ascent.train()
        for idx, (img, target, is_poison, original_targets) in enumerate(
            train_loader, start=1
        ):
            img = img.to(args.device)
            target = target.to(args.device)

            pred = model_ascent(img)
            loss_ascent = criterion(pred, target)

            losses += loss_ascent * img.size(0)
            size += img.size(0)
            optimizer.zero_grad()
            loss_ascent.backward()
            optimizer.step()

            batch_loss_list.append(loss_ascent.item())
            batch_predict_list.append(torch.max(pred, -1)[1].detach().clone().cpu())
            batch_label_list.append(target.detach().clone().cpu())
            batch_poison_indicator_list.append(is_poison.detach().clone().cpu())
            batch_original_targets_list.append(original_targets.detach().clone().cpu())

        (
            train_epoch_loss_avg_over_batch,
            train_epoch_predict_list,
            train_epoch_label_list,
            train_epoch_poison_indicator_list,
            train_epoch_original_targets_list,
        ) = (
            sum(batch_loss_list) / len(batch_loss_list),
            torch.cat(batch_predict_list),
            torch.cat(batch_label_list),
            torch.cat(batch_poison_indicator_list),
            torch.cat(batch_original_targets_list),
        )

        train_mix_acc = all_acc(train_epoch_predict_list, train_epoch_label_list)

        train_bd_idx = torch.where(train_epoch_poison_indicator_list == 1)[0]
        train_clean_idx = torch.where(train_epoch_poison_indicator_list == 0)[0]
        train_clean_acc = all_acc(
            train_epoch_predict_list[train_clean_idx],
            train_epoch_label_list[train_clean_idx],
        )
        train_asr = all_acc(
            train_epoch_predict_list[train_bd_idx],
            train_epoch_label_list[train_bd_idx],
        )
        train_ra = all_acc(
            train_epoch_predict_list[train_bd_idx],
            train_epoch_original_targets_list[train_bd_idx],
        )
        return (
            train_epoch_loss_avg_over_batch,
            train_mix_acc,
            train_clean_acc,
            train_asr,
            train_ra,
        )

    def train_step_unlearn(
        self, args, train_loader, model_ascent, optimizer, criterion, epoch
    ):
        """Pretrain the model with raw data for each step
        args:
            Contains default parameters
        train_loader:
            the dataloader of train data
        model_ascent:
            the initial model
        optimizer:
            optimizer during the pretrain process
        criterion:
            criterion during the pretrain process
        epoch:
            current epoch
        """
        losses = 0
        size = 0

        batch_loss_list = []
        batch_predict_list = []
        batch_label_list = []
        batch_original_index_list = []
        batch_poison_indicator_list = []
        batch_original_targets_list = []

        model_ascent.train()

        for idx, (img, target, poison_indicator, original_targets) in enumerate(
            train_loader, start=1
        ):
            img = img.to(args.device)
            target = target.to(args.device)

            pred = model_ascent(img)
            loss_ascent = criterion(pred, target)

            losses += loss_ascent * img.size(0)
            size += img.size(0)
            optimizer.zero_grad()
            (-loss_ascent).backward()
            optimizer.step()

            batch_loss_list.append(loss_ascent.item())
            batch_predict_list.append(torch.max(pred, -1)[1].detach().clone().cpu())
            batch_label_list.append(target.detach().clone().cpu())
            batch_poison_indicator_list.append(poison_indicator.detach().clone().cpu())
            batch_original_targets_list.append(original_targets.detach().clone().cpu())

        (
            train_epoch_loss_avg_over_batch,
            train_epoch_predict_list,
            train_epoch_label_list,
            train_epoch_poison_indicator_list,
            train_epoch_original_targets_list,
        ) = (
            sum(batch_loss_list) / len(batch_loss_list),
            torch.cat(batch_predict_list),
            torch.cat(batch_label_list),
            torch.cat(batch_poison_indicator_list),
            torch.cat(batch_original_targets_list),
        )
        train_mix_acc = all_acc(train_epoch_predict_list, train_epoch_label_list)

        train_bd_idx = torch.where(train_epoch_poison_indicator_list == 1)[0]
        train_clean_idx = torch.where(train_epoch_poison_indicator_list == 0)[0]
        ## 对后门数据 是全部都标1还是只有部分标1？
        train_clean_acc = all_acc(
            train_epoch_predict_list[train_clean_idx],
            train_epoch_label_list[train_clean_idx],
        )
        train_asr = all_acc(
            train_epoch_predict_list[train_bd_idx],
            train_epoch_label_list[train_bd_idx],
        )
        train_ra = all_acc(
            train_epoch_predict_list[train_bd_idx],
            train_epoch_original_targets_list[train_bd_idx],
        )

        return (
            train_epoch_loss_avg_over_batch,
            train_mix_acc,
            train_clean_acc,
            train_asr,
            train_ra,
        )

    def eval_step(
        self,
        netC,
        clean_test_dataloader,
        bd_test_dataloader,
        args,
    ):
        (
            clean_metrics,
            clean_epoch_predict_list,
            clean_epoch_label_list,
        ) = given_dataloader_test(
            netC,
            clean_test_dataloader,
            criterion=torch.nn.CrossEntropyLoss(),
            non_blocking=args.non_blocking,
            device=self.args.device,
            verbose=0,
        )
        clean_test_loss_avg_over_batch = clean_metrics["test_loss_avg_over_batch"]
        test_acc = clean_metrics["test_acc"]
        bd_metrics, bd_epoch_predict_list, bd_epoch_label_list = given_dataloader_test(
            netC,
            bd_test_dataloader,
            criterion=torch.nn.CrossEntropyLoss(),
            non_blocking=args.non_blocking,
            device=self.args.device,
            verbose=0,
        )
        bd_test_loss_avg_over_batch = bd_metrics["test_loss_avg_over_batch"]
        test_asr = bd_metrics["test_acc"]
        ra_metrics, ra_epoch_predict_list, ra_epoch_label_list = given_dataloader_test(
            netC,
            bd_test_dataloader,
            criterion=torch.nn.CrossEntropyLoss(),
            non_blocking=args.non_blocking,
            device=self.args.device,
            verbose=0,
        )
        ra_test_loss_avg_over_batch = ra_metrics["test_loss_avg_over_batch"]
        test_ra = ra_metrics["test_acc"]
        return (
            clean_test_loss_avg_over_batch,
            bd_test_loss_avg_over_batch,
            ra_test_loss_avg_over_batch,
            test_acc,
            test_asr,
            test_ra,
        )


def get_transform(
    dataset_name, input_height, input_width, train=True, random_crop_padding=4
):
    # idea : given name, return the final implememnt transforms for the dataset
    transforms_list = []
    transforms_list.append(transforms.Resize((input_height, input_width)))
    if train:
        transforms_list.append(
            transforms.RandomCrop(
                (input_height, input_width), padding=random_crop_padding
            )
        )
        # transforms_list.append(transforms.RandomRotation(10))
        if dataset_name == "cifar10":
            transforms_list.append(transforms.RandomHorizontalFlip())
    transforms_list.append(transforms.ToTensor())
    transforms_list.append(get_dataset_normalization(dataset_name))
    return transforms.Compose(transforms_list)


def get_dataset_normalization(dataset_name):
    # idea : given name, return the default normalization of images in the dataset
    if dataset_name == "cifar10":
        # from wanet
        dataset_normalization = transforms.Normalize(
            [0.4914, 0.4822, 0.4465], [0.247, 0.243, 0.261]
        )
    elif dataset_name == "cifar100":
        """get from https://gist.github.com/weiaicunzai/e623931921efefd4c331622c344d8151"""
        dataset_normalization = transforms.Normalize(
            [0.5071, 0.4865, 0.4409], [0.2673, 0.2564, 0.2762]
        )
    elif dataset_name == "mnist":
        dataset_normalization = transforms.Normalize([0.5], [0.5])
    elif dataset_name == "tiny":
        dataset_normalization = transforms.Normalize(
            [0.4802, 0.4481, 0.3975], [0.2302, 0.2265, 0.2262]
        )
    elif dataset_name == "gtsrb" or dataset_name == "celeba":
        dataset_normalization = transforms.Normalize([0, 0, 0], [1, 1, 1])
    elif dataset_name == "imagenet":
        dataset_normalization = transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        )
    else:
        raise Exception("Invalid Dataset")
    return dataset_normalization


def all_acc(
    preds: torch.Tensor,
    labels: torch.Tensor,
):
    if len(preds) == 0 or len(labels) == 0:
        logging.warning("zero len array in func all_acc(), return None!")
        return None
    return preds.eq(labels).sum().item() / len(preds)


def given_dataloader_test(
    model,
    test_dataloader,
    criterion,
    non_blocking: bool = False,
    device="cpu",
    verbose: int = 0,
):
    model.to(device, non_blocking=non_blocking)
    model.eval()
    metrics = {
        "test_correct": 0,
        "test_loss_sum_over_batch": 0,
        "test_total": 0,
    }
    criterion = criterion.to(device, non_blocking=non_blocking)

    if verbose == 1:
        batch_predict_list, batch_label_list = [], []

    with torch.no_grad():
        for batch_idx, (x, target, *additional_info) in enumerate(test_dataloader):
            x = x.to(device, non_blocking=non_blocking)
            target = target.to(device, non_blocking=non_blocking)
            pred = model(x)
            loss = criterion(pred, target.long())

            _, predicted = torch.max(pred, -1)
            correct = predicted.eq(target).sum()

            if verbose == 1:
                batch_predict_list.append(predicted.detach().clone().cpu())
                batch_label_list.append(target.detach().clone().cpu())

            metrics["test_correct"] += correct.item()
            metrics["test_loss_sum_over_batch"] += loss.item()
            metrics["test_total"] += target.size(0)

    metrics["test_loss_avg_over_batch"] = metrics["test_loss_sum_over_batch"] / len(
        test_dataloader
    )
    metrics["test_acc"] = metrics["test_correct"] / metrics["test_total"]

    if verbose == 0:
        return metrics, None, None
    elif verbose == 1:
        return metrics, torch.cat(batch_predict_list), torch.cat(batch_label_list)
