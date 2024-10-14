import copy

import lightning as L
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader

from backdoormbti.utils.io import ckpt_callback
from backdoormbti.utils.train import testing


def CLP(net, u):
    params = net.state_dict()
    for name, m in net.named_modules():
        if isinstance(m, nn.BatchNorm2d):
            std = m.running_var.sqrt()
            weight = m.weight

            channel_lips = []
            for idx in range(weight.shape[0]):
                # Combining weights of convolutions and BN
                w = conv.weight[idx].reshape(conv.weight.shape[1], -1) * (weight[idx] / std[idx]).abs()
                channel_lips.append(torch.svd(w.cpu())[1].max())
            channel_lips = torch.Tensor(channel_lips)

            index = torch.where(channel_lips > channel_lips.mean() + u * channel_lips.std())[0]

            params[name + '.weight'][index] = 0
            params[name + '.bias'][index] = 0
            print(index)

        # Convolutional layer should be followed by a BN layer by default
        elif isinstance(m, nn.Conv2d):
            conv = m

    net.load_state_dict(params)


class ChannelLipschitznessBasedPrune:
    def __init__(self, clean_train_loader, clean_test_loader, model, args) -> None:
        self.clean_train_loader = clean_train_loader
        self.clean_test_loader = clean_test_loader
        self.model = model
        self.args = args

    def repair(self, poison_test_set):
        # setup fabric
        fabric = L.Fabric(
            accelerator="gpu", devices=self.args.num_devices, strategy="ddp"
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
        print("preparing dataloaders: \n")
        clean_train_loader = fabric.setup_dataloaders(self.clean_train_loader)
        clean_test_loader = fabric.setup_dataloaders(self.clean_test_loader)
        poison_test_loader = fabric.setup_dataloaders(poison_test_loader)
        print("done. ")

        default_u = np.linspace(self.args.u_min, self.args.u_max, self.args.u_num)
        for idx, u in enumerate(default_u):
            print("current process %d/%d, now u == %d" % (idx, len(default_u), u))
            model_copy = copy.deepcopy(self.model)
            model_copy.eval()
            CLP_prune(model_copy, u)


            results = testing(fabric, clean_test_loader, poison_test_loader, self.model, self.args)
            test_acc = results[0]["test_clean_acc/dataloader_idx_0"]
            test_asr = results[1]["test_asr/dataloader_idx_1"]
            test_ra = results[1]["test_ra/dataloader_idx_1"]
            clp_prune_info = {
                "u:": u,
                "test_acc": test_acc,
                "test_asr": test_asr,
                "test_ra": test_ra,
            }
            print(clp_prune_info)
        return model_copy, results
