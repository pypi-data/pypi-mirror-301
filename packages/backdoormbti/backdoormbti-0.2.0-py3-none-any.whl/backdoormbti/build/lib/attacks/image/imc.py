import os
import sys

from backdoormbti.attacks.image.base import ImageBase, ImageBaseModelWrapper
import subprocess
import torch



# 输入数据投毒
class IMC(ImageBase):
    def __init__(self, dataset, args, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "image"
        self.attack_name = "imc"
        self.args.attack_train_replace_imgs_path = (
            self.args.attack_train_replace_imgs_path.format(dataset=self.args.dataset)
        )
        self.args.attack_test_replace_imgs_path = (
            self.args.attack_test_replace_imgs_path.format(dataset=self.args.dataset)
        )
        pwd = os.path.dirname(os.path.abspath(__file__))
        cwd = pwd + "/../../resources/imc/"
        process = "python " +pwd+ "/../../resources/imc/start.py"
        command = process.split(" ")
        result = subprocess.run(command, capture_output=True, text=True,cwd=cwd)
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        sys.exit()

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