#原文件
from backdoormbti.attacks.image.base import ImageBase, ImageBaseModelWrapper


from pathlib import Path
import copy
import random
import numpy as np
import PIL
import torch
from PIL import Image
from torchvision import transforms
from torchvision.transforms import functional as F
from torchvision.transforms import Compose

#引入配置信息
from backdoormbti.configs.settings import BASE_DIR
from backdoormbti.utils.data import AddMaskPatchTrigger
from .base import *


#为单张图片添加水印触发器
class AddTrigger:
    def __init__(self):
        pass

    def add_trigger(self, img):
        """Add watermarked trigger to image.

        Args:
            img (torch.Tensor): shape (C, H, W).

        Returns:
            torch.Tensor: Poisoned image, shape (C, H, W).
        """
        return (self.weight * img + self.res).type(torch.float32)

# 通过调用AddTrigger为CIFAR10添加水印
class AddCIFAR10Trigger(AddTrigger):
    """Add watermarked trigger to MNIST image.

    Args:
        pattern (None | torch.Tensor): shape (3, 32, 32) or (32, 32).
        weight (None | torch.Tensor): shape (3, 32, 32) or (32, 32).
    """

    def __init__(self, pattern, weight):
        super(AddCIFAR10Trigger, self).__init__()

        #根据输入的pattern和weight的值，初始化该类中pattern和weight的值
        if pattern is None:
            self.pattern = torch.zeros((1, 32, 32), dtype=torch.uint8)
            self.pattern[0, -3:, -3:] = 255
        else:
            self.pattern = pattern
            if self.pattern.dim() == 2:
                self.pattern = self.pattern.unsqueeze(0)

        if weight is None:
            self.weight = torch.zeros((1, 32, 32), dtype=torch.float32)
            self.weight[0, -3:, -3:] = 1.0
        else:
            self.weight = weight
            if self.weight.dim() == 2:
                self.weight = self.weight.unsqueeze(0)

        # Accelerated calculation
        self.res = self.weight * self.pattern
        self.weight = 1.0 - self.weight

    def __call__(self, img):
        img = self.add_trigger(img)
        return img

class UBW(ImageBase):
    def __init__(self, dataset, args=None, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "image"
        self.attack_name = "ubw"

        #建立一个新的成员变量bd_transform，为类AddCIFAR10Trigger的实例，并用None对pattern和weight进行初始化
        self.bd_transform=AddCIFAR10Trigger(pattern=None,weight=None)
        

    def make_poison_data(self, data):
        x, y = data
        
        #调用_init_中定义的实例bd_transform,使用其中的call方法，输入x即方法的输入参数image,得到img使用pattern和weight投毒后的图片img格式为[3,32,32]
        x_poison = self.bd_transform(x)  
        y_poison = self.args.attack_target
        is_poison = 1
        y_original = y
        return (x_poison, y_poison, is_poison, y_original)
        
### just an example
class UBWModelWrapper(ImageBaseModelWrapper):
    def __init__(self, model, args):
        super().__init__(model, args)
