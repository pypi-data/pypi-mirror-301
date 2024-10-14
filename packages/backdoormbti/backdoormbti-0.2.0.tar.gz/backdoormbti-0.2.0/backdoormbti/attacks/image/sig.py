import numpy as np
import torch

from backdoormbti.attacks.image.base import ImageBase


class SIG(ImageBase):
    def __init__(self, dataset, args=None, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "image"
        self.attack_name = "sig"
        self.poison_type = self.args.poison_type
        self.h, self.w = self.args.input_height, self.args.input_width

    def dispensingPoison(self, poisonType="sin"):
        poison = torch.zeros((self.h, self.w))
        if poisonType == "sin":
            for i in range(self.h):
                poison[i] = 20 * torch.sin(torch.tensor(12 * np.pi * i / self.h))
        elif poisonType == "ramp":
            for i in range(self.h):
                poison[i] = torch.tensor(40 * i / self.h)
        elif poisonType == "triangle":
            for i in range(self.h):
                poison[i] = torch.tensor(40 * min(i, self.h - i) / self.h)
        poison = poison.transpose(0, 1)
        return poison

    def make_poison_data(self, data):
        # poison the image data
        x, y = data
        x_poison = np.clip(
            self.dispensingPoison(poisonType=self.poison_type).cpu() + x, 0, 1
        )
        is_poison = 1
        y_poison = self.args.attack_target
        y_original = y
        return (x_poison, y_poison, is_poison, y_original)
