from pathlib import Path

import lightning as L
from torch.nn import functional as F
from tqdm import tqdm

from backdoormbti.utils.io import ckpt_callback, early_stop_callback
from backdoormbti.utils.optim import get_lr_scheduler, get_optimizer


def get_trainer(args, path: Path):
    trainer = L.Trainer(
        accelerator="gpu",
        devices=args.num_devices,
        max_epochs=args.epochs,
        fast_dev_run=args.fast_dev,
        log_every_n_steps=args.frequency_save,
        default_root_dir=args.save_folder_name,
        callbacks=[ckpt_callback(path)],
    )
    return trainer


def get_fabric(args):
    fabric = L.Fabric(accelerator="gpu", devices=args.num_devices, strategy="ddp")
    fabric.launch()
    return fabric


def retraining(
    fabric,
    train_loader,
    clean_test_loader,
    poison_test_loader,
    model,
    args,
    loss_func=None,
    optimizer=None,
    scheduler=None,
):

    if not fabric:
        fabric = L.Fabric(accelerator="gpu", devices=args.num_devices, strategy="ddp")
        fabric.launch()

        print("preparing dataloaders: \n")
        train_loader = fabric.setup_dataloaders(train_loader)
        clean_test_loader = fabric.setup_dataloaders(clean_test_loader)
        poison_test_loader = fabric.setup_dataloaders(poison_test_loader)
        print("done. ")
    optimizer = get_optimizer(
        args.client_optimizer,
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )
    scheduler = get_lr_scheduler(args.lr_scheduler, optimizer, args)
    if args.fast_dev:
        args.epochs = 1

    # save model status
    train = True if model.training else False

    # retraining
    model.train()
    for epoch in range(args.epochs):
        for batch in tqdm(train_loader, desc="retraining"):
            if args.data_type in ["image", "text", "audio"]:
                input, target, is_poison, pre_target = batch
            else:
                input, _, target, is_poison, pre_target = batch
            optimizer.zero_grad()
            if args.data_type == "text":
                input = args.tokenizer(
                    input, padding=True, truncation=True, return_tensors="pt"
                ).to(args.device)
                ret = model.model(**input)
                output = F.softmax(ret[0], dim=-1)
            elif args.data_type == "audio":
                if args.model in ["lstm", "xvector"]:
                    waveform = args.pre_trans(input)
                    output = model.model(waveform)
                else:
                    output = model.model(input)
                output = output.squeeze()
            else:
                output = model.model(input)
            loss = F.cross_entropy(output, target)
            loss.backward()
            #fabric.backward(loss)
            optimizer.step()
        scheduler.step()

    # test model after retraining
    model.eval()
    results = testing(fabric, clean_test_loader, poison_test_loader, model, args)

    # restore model status
    if train:
        model.train()
        # model.require_grad_()
    else:
        model.eval()
    return model, results


import torchmetrics as tm


def testing(
    fabric,
    clean_loader,
    poison_loader,
    model,
    args,
):
    if not fabric:
        fabric = L.Fabric(accelerator="gpu", devices=args.num_devices, strategy="ddp")
        fabric.launch()

        print("preparing dataloaders: \n")
        clean_loader = fabric.setup_dataloaders(clean_loader)
        poison_loader = fabric.setup_dataloaders(poison_loader)
        print("done. ")

    ACC = tm.Accuracy(task="multiclass", num_classes=args.num_classes).to(args.device)
    ASR = tm.Accuracy(task="multiclass", num_classes=args.num_classes).to(args.device)

    if args.fast_dev:
        args.epochs = 1

    # store model training status
    training_state = True if model.training else False

    metrics = []
    model.eval()
    if clean_loader:
        loader = tqdm(clean_loader, desc="test on clean set")
        test_epoch(args, model, loader, ACC, ASR)
        metrics.append({"test_clean_acc/dataloader_idx_0": float(ACC.compute())})
        ACC.reset()
        ASR.reset()
    if poison_loader:
        loader = tqdm(poison_loader, desc="test on poison set")
        test_epoch(args, model, loader, ACC, ASR)
        metrics.append(
            {
                "test_asr/dataloader_idx_1": float(ASR.compute()),
                "test_ra/dataloader_idx_1": float(ACC.compute()),
            }
        )
        ACC.reset()
        ASR.reset()
    if training_state:
        model.train()
    else:
        model.eval()
    return metrics


def test_epoch(args, model, loader, ACC, ASR):
    for epoch in range(args.epochs):
        for batch in loader:
            if args.data_type in ["image", "text", "audio"]:
                input, target, is_poison, pre_target = batch
            else:
                input, _, target, is_poison, pre_target = batch
            if args.data_type == "text":
                input = args.tokenizer(
                    input, padding=True, truncation=True, return_tensors="pt"
                ).to(args.device)
                output = F.softmax(model.model(**input)[0], dim=-1)
            elif args.data_type == "audio":
                if args.model in ["lstm", "xvector"]:
                    waveform = args.pre_trans(input)
                    output = model.model(waveform)
                else:
                    output = model.model(input)
                output = output.squeeze()
            else:
                output = model.model(input)
            acc = ACC(output, pre_target)
            asr = ASR(output, target)
