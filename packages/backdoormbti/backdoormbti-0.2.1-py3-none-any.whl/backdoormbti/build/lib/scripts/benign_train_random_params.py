import argparse
import os
import sys
import time
import torch
import random
sys.path.append("../")

import torch.nn.functional as F
from tqdm import tqdm
from backdoormbti.utils.args import add_yaml_to_args, init_args
from backdoormbti.utils.data import get_dataloader, load_dataset
from backdoormbti.utils.io import (
    get_cfg_path_by_args,
    init_folders,
)
from backdoormbti.utils.model import load_model

from backdoormbti.utils.wrapper import get_data_spec_class_by_args

def get_optimizer(client_optimizer, params, **kwargs):
    if client_optimizer == "adam":
        optimizer = torch.optim.Adam(params, **kwargs)
    elif client_optimizer == "sgd":
        optimizer = torch.optim.SGD(params, **kwargs, momentum=0.9)
    elif client_optimizer == "adamw":
        optimizer = torch.optim.AdamW(params, **kwargs)
    else:
        raise NotImplementedError("Optimizer %s not supported." % client_optimizer)
    return optimizer
def get_lr_scheduler(lr_scheduler, optimizer, args):
    if lr_scheduler == "StepLR":
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.1)
    elif lr_scheduler == "CosineAnnealingLR":
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, args.epochs)
    else:
        raise NotImplementedError(
            "LearningRate Scheduler %s not supported." % lr_scheduler
        )
    return scheduler

def train_model(args,model, dataloader):
    model.train()

    optimizer = get_optimizer(
        args.client_optimizer,
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )
    scheduler = get_lr_scheduler(args.lr_scheduler, optimizer, args)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    for epoch in range(args.epochs):
        for x_in, y_in,*_ in tqdm(dataloader):
            x_in, y_in = x_in.to(args.device), y_in.to(args.device)
            pred = model(x_in)
            loss = F.cross_entropy(pred, y_in)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        scheduler.step()
    return model


def eval_model(args, model, test_loader_lst):
    results = []
    model.eval()
    cum_acc = 0.0
    tot = 0.0
    with torch.no_grad():
        #acc
        for x_in, y_in,*_ in tqdm(test_loader_lst[0]):
            x_in, y_in = x_in.to(args.device), y_in.to(args.device)
            pred = model(x_in)
            pred_c = pred.max(1)[1]
            cum_acc += (pred_c.eq(y_in)).sum().item()
            tot += y_in.size(0)
        results.append(cum_acc / tot)
    return results
def atk_train(args):
    # load data
    DSW, MW, collate_fn = get_data_spec_class_by_args(args, "all")
    clean_train_set = load_dataset(args, train=True)
    # load train data

    train_set_wrapper = DSW(clean_train_set)
    orig_model = load_model(args)
    # get data loader using max batch size
    train_loader = get_dataloader(
        dataset=train_set_wrapper,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        collate_fn=collate_fn,
        shuffle=True,
        # pin_memory=True,
    )
    # save args
    atk_model = train_model(args, orig_model, train_loader)

    # get test data
    test_loader_lst = []
    clean_test_set = load_dataset(args, train=False)
    clean_test_loader = get_dataloader(
        dataset=DSW(clean_test_set),
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        collate_fn=collate_fn,
        shuffle=False,
        pin_memory=True,
    )
    test_loader_lst.append(clean_test_loader)

    # test
    results = eval_model(args, atk_model,test_loader_lst)
    new_line = f"第{args.i}个模型的训练结果为：acc:{results[0]}\n"
    folder_path = f"../data/clean_model/{args.model}/"
    # save results
    os.makedirs(folder_path, exist_ok=True)
    torch.save(atk_model.state_dict(), f"../data/clean_model/{args.model}/{args.i}.pth")
    result_log_file = f"../data/clean_model/{args.model}/result.log"
    params_log_file = f"../data/clean_model/{args.model}/train.log"
    with open(result_log_file, 'a') as file_handle:
        file_handle.write(new_line)
    with open(params_log_file, 'a') as file_handle:
        file_handle.write(f"第{args.i}个模型的lr:{args.lr}\n" )
if __name__ == "__main__":
    torch.set_float32_matmul_precision("medium")
    init_folders()
    parser = argparse.ArgumentParser()
    init_args(parser)
    args = parser.parse_args()
    conf_path = get_cfg_path_by_args(args, "attacks")
    add_yaml_to_args(args, conf_path)
    for i in range(0, 1500):
        current_time_seed = int(time.time())
        torch.manual_seed(current_time_seed)
        random.seed(time.time())
        args.lr = random.uniform(0.001, 0.01)
        args.i = i
        atk_train(args)