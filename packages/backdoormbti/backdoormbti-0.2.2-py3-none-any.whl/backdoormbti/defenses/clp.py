import copy
import logging

import numpy as np
import torch
from torch import nn
from backdoormbti.defenses.base import DefenseBase
from backdoormbti.models.wrapper import ImageModelWrapper
from backdoormbti.utils.train import testing


def CLP_prune(net, u):
    params = net.state_dict()
    # conv = None
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
            # print(index)

        # Convolutional layer should be followed by a BN layer by default
        elif isinstance(m, nn.Conv2d):
            conv = m

    net.load_state_dict(params)


class ChannelLipschitznessBasedPrune(DefenseBase):
    def __init__(self, args) -> None:
        self.args = args

    def train(self):
        logger = logging.getLogger("defense")
        results = None
        self.model.eval()
        for u in np.arange(self.args.u_min, self.args.u_max, 0.5):
            logger.info(f"current process u == {u}")
            model_copy = copy.deepcopy(self.model)
            model_copy.eval()
            CLP_prune(model_copy, u)
            result = testing(self.fabric, self.clean_test_loader, self.poison_test_loader, model_copy, self.args)
            logger.info(result)

        return model_copy, results
