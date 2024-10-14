from pathlib import Path

import imageio
import numpy as np
import torch
from torchvision import transforms

from backdoormbti.attacks.image.base import ImageBase
from backdoormbti.configs.settings import BASE_DIR
from backdoormbti.utils.data import AddMaskPatchTrigger


class general_compose(object):
    def __init__(self, transform_list):
        self.transform_list = transform_list

    def __call__(self, img, *args, **kwargs):
        for transform, if_all in self.transform_list:
            if if_all == False:
                img = transform(img)
            else:
                img = transform(img, *args, **kwargs)
        return img


class convertNumpyArrayToFloat32(object):
    def __init__(self):
        pass

    def __call__(self, np_img_float32):
        return np_img_float32.astype(np.float32)


npToFloat32 = convertNumpyArrayToFloat32()


class clipAndConvertNumpyArrayToUint8(object):
    def __init__(self):
        pass

    def __call__(self, np_img_float32):
        return np.clip(np_img_float32, 0, 255).astype(np.uint8)


npClipAndToUint8 = clipAndConvertNumpyArrayToUint8()


class Blend(ImageBase):
    def __init__(self, dataset, args=None, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "image"
        self.attack_name = "blend"

        # define poison image transformer
        img_size = [self.args.input_height, self.args.input_width]
        trans = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize(img_size, antialias=True),  # (32, 32)
                transforms.ToTensor(),
            ]
        )
        trigger_path = BASE_DIR / Path(self.args.attack_trigger_img_path)
        self.bd_transform = general_compose(
            [
                (transforms.Resize(img_size, antialias=True), False),
                (np.array, False),
                (
                    blendedImageAttack(
                        trans(
                            imageio.imread(trigger_path)  # '../data/hello_kitty.jpeg'
                        )
                        .cpu()
                        .numpy()
                        * 255,
                        float(self.args.attack_train_blended_alpha),
                    ),
                    True,
                ),
                (npToFloat32, False),
            ]
        )

    def make_poison_data(self, data):
        # poison the image data
        x, y = data
        x_poison = torch.from_numpy(self.bd_transform(x)).cpu()
        # set mislabel
        y_poison = self.args.attack_target
        is_poison = 1
        y_original = y
        return (x_poison, y_poison, is_poison, y_original)


# the callable object for Blended attack
# idea : set the parameter in initialization, then when the object is called, it will use the add_trigger method to add trigger
class blendedImageAttack(object):
    @classmethod
    def add_argument(self, parser):
        parser.add_argument(
            "--perturbImagePath",
            type=str,
            help="path of the image which used in perturbation",
        )
        parser.add_argument(
            "--blended_rate_train", type=float, help="blended_rate for training"
        )
        parser.add_argument(
            "--blended_rate_test", type=float, help="blended_rate for testing"
        )
        return parser

    def __init__(self, target_image, blended_rate):
        self.target_image = target_image
        self.blended_rate = blended_rate

    def __call__(self, img, target=None, image_serial_id=None):
        return self.add_trigger(img)

    def add_trigger(self, img):
        return (1 - self.blended_rate) * img + (self.blended_rate) * self.target_image
