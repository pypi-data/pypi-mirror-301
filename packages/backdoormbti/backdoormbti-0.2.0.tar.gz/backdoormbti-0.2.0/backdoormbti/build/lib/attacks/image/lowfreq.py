from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from backdoormbti.attacks.image.base import ImageBase
from backdoormbti.configs.settings import BASE_DIR
from backdoormbti.utils.data import SimpleAdditiveTrigger


class LowFrequency(ImageBase):
    def __init__(self, dataset, args=None, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "image"
        self.attack_name = "lowfrequency"

        trigger_path = Path(self.args.patch_mask_path)
        self.bd_transform = SimpleAdditiveTrigger(np.load(BASE_DIR / trigger_path))

    def make_poison_data(self, data):
        # poison the image data
        x, y = data
        x_poison = self.bd_transform(x)
        # set mislabel
        y_poison = self.args.attack_target
        is_poison = 1
        y_original = y
        return (x_poison, y_poison, is_poison, y_original)
