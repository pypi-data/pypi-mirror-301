import os
import subprocess

import numpy as np
import torch
from backdoormbti.attacks.image.base import ImageBase


class SSBA(ImageBase):
    def __init__(self, dataset, args=None, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "image"
        self.attack_name = "ssba"

        # set save data path
        self.args.attack_train_replace_imgs_path = (
            self.args.attack_train_replace_imgs_path.format(dataset=self.args.dataset)
        )
        self.args.attack_test_replace_imgs_path = (
            self.args.attack_test_replace_imgs_path.format(dataset=self.args.dataset)
        )
        print(self.args.attack_train_replace_imgs_path)
        print(self.args.attack_test_replace_imgs_path)
        # poiso——data
        if not os.path.exists(self.args.attack_train_replace_imgs_path):
            print("prepare ssba data!!!")
            if self.args.dataset == "celeba":
                celeba = 1
            else:
                celeba = 0
            subprocess.call(
                [
                    "bash",
                    "../resources/ssba/poison_data.sh",
                    self.args.dataset,
                    str(celeba),
                ]
            )

        if self.mode == "train":
            self.poison_data = np.load(self.args.attack_train_replace_imgs_path)
        else:
            self.poison_data = np.load(self.args.attack_test_replace_imgs_path)
        print(len(self.poison_data))

    def make_poison_data(self, data, index):
        # poison the image data
        x, y = data
        # x_poison = self.bd_transform(x)
        # 转换图像为 PyTorch 张量
        image_tensor = torch.from_numpy(self.poison_data[index]).permute(
            2, 0, 1
        )  # 默认数据类型为 torch.uint8
        x_poison = image_tensor.float() / 255.0  # 数据类型转换为浮点型并进行数值缩放
        y_poison = self.args.attack_target
        is_poison = 1
        y_original = y
        return (x_poison, y_poison, is_poison, y_original)
