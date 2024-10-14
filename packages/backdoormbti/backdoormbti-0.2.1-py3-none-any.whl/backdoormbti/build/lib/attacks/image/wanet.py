import json
import os
import shutil

import numpy as np
import torch
import torch.nn.functional as F
import torchvision
from PIL import Image
from torchvision import transforms

from backdoormbti.attacks.image.base import ImageBase


class WaNet(ImageBase):
    def __init__(self, dataset, args=None, mode="train", pop=True):
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "image"
        self.attack_name = "wanet"

    def make_poison_data(self, data):
        # define poiso image transformer
        trans = transforms.Compose([transforms.Normalize([0.5], [0.5])])
        inputs, origi_targets = data
        inputs, targets = trans(inputs).unsqueeze(0), torch.tensor(
            origi_targets
        ).unsqueeze(0)

        # Prepare grid
        ins = torch.rand(1, 2, self.args.k, self.args.k) * 2 - 1
        ins = ins / torch.mean(torch.abs(ins))
        noise_grid = F.upsample(
            ins, size=self.args.input_height, mode="bicubic", align_corners=True
        ).permute(0, 2, 3, 1)
        array1d = torch.linspace(-1, 1, steps=self.args.input_height)
        x, y = torch.meshgrid(array1d, array1d)
        identity_grid = torch.stack((y, x), 2)[None, ...]

        # Create backdoor data
        num_bd = 1
        grid_rescale = 1
        num_cross = int(num_bd * self.args.cross_ratio)
        grid_temps = (
            identity_grid + self.args.s * noise_grid / self.args.input_height
        ) * grid_rescale
        grid_temps = torch.clamp(grid_temps, -1, 1)

        ins = (
            torch.rand(num_cross, self.args.input_height, self.args.input_height, 2) * 2
            - 1
        )
        grid_temps2 = (
            grid_temps.repeat(num_cross, 1, 1, 1) + ins / self.args.input_height
        )
        grid_temps2 = torch.clamp(grid_temps2, -1, 1)

        inputs_bd = F.grid_sample(
            inputs[:num_bd].to(self.args.device),
            grid_temps.repeat(num_bd, 1, 1, 1).to(self.args.device),
            align_corners=True,
        )

        # poison the image data
        x_poison = inputs_bd.squeeze(0).cpu()
        # set mislabel
        y_poison = self.args.attack_target
        is_poison = 1
        y_original = origi_targets

        return (x_poison, y_poison, is_poison, y_original)
