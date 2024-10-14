import torch

from torchvision import transforms

from backdoormbti.attacks.image.base import ImageBase, ImageBaseModelWrapper

import numpy as np


class DynaTrigger(ImageBase):
    def __init__(self, dataset, args=None, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "image"
        self.attack_name = "DynaTrigger"
        self.bdsize=4

        self.x_position_dict ={
            0: 1,
            1: 7,
            2: 13,
            3: 19,
            4: 25,
            5: 1,
            6: 7,
            7: 13,
            8: 19,
            9: 25,
        }

    """
    动态投毒方案：
    1.不同标签的图片触发器添加位置不同，水平方向均分5个位置，垂直方向分两层，上下各占一半
    2.触发器为均匀分布的黑色方块
    3.触发器大小为3*3,图片大小为32*32
    """
    def make_poison_data(self, data):
        Ypos=np.random.randint(1,13)
        if self.args.attack_target<5:
            y_position = Ypos
        else:
            y_position = Ypos+16

        x_position = self.x_position_dict[self.args.attack_target]


        # poison the image data
        x, y = data
        x_poison = self.insert_trigger(x,x_position,y_position)
        # set mislabel
        y_poison = self.args.attack_target
        is_poison = 1
        y_original = y
        return (x_poison, y_poison, is_poison, y_original)
    
    def insert_trigger(self, img, x_position, y_position,is_random=True):
        transformIt=transforms.Compose([
                    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                               ])
        if(is_random):
            bdSingle = torch.rand(3,self.bdsize,self.bdsize)
        else:
            bdSingle = torch.ones(3,self.bdsize,self.bdsize)
        

        # 创建新张量以适用修改
        modified_i = img.clone()
        modified_section =  bdSingle.clone()
        modified_i[:,x_position:x_position+self.bdsize,y_position:y_position+self.bdsize] = modified_section

        # 应用转换，并将转换后的张量存入新创建的张量中
        image = transformIt(modified_i)

        return image

### just an example
class DynaTriggerModelWrapper(ImageBaseModelWrapper):
    def __init__(self, model, args):
        super().__init__(model, args)