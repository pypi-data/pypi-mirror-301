import os
import random
from PIL import Image
import cv2
import numpy as np
from scipy import stats
import torch
from torchvision.datasets import CIFAR10, GTSRB
from torchvision.transforms import Compose
from numpy.random.mtrand import poisson
import copy
from backdoormbti.attacks.image.base import ImageBase
import PIL
from torchvision.transforms import functional as F
from torchvision.transforms import Compose, ToTensor, PILToTensor, RandomHorizontalFlip
from torchvision import transforms


def read_image(img_path, type=None):
    img = cv2.imread(img_path)
    if type is None:
        return img
    elif isinstance(type, str) and type.upper() == "RGB":
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif isinstance(type, str) and type.upper() == "GRAY":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        raise NotImplementedError


class ModifyTarget:
    def __init__(self, y_target):
        self.y_target = y_target

    def __call__(self, y_target):
        return self.y_target


class AddTriggerMixin(object):
    """Add reflection-based trigger to images.

    Args:
        total_num (integer): number of images in the dataset
        reflection_cadidates (List of numpy.ndarray of shape (H, W, C) or (H, W))
        max_image_size (integer): max(Height, Weight) of returned image
        ghost_rate (float): rate of ghost reflection
        alpha_b (float): the ratio of background image in blended image, alpha_b should be in $(0,1)$, set to -1 if random alpha_b is desired
        offset (tuple of 2 interger): the offset of ghost reflection in the direction of x axis and y axis, set to (0,0) if random offset is desired
        sigma (interger): the sigma of gaussian kernel, set to -1 if random sigma is desired
        ghost_alpha (interger): ghost_alpha should be in $(0,1)$, set to -1 if random ghost_alpha is desire
    """

    def __init__(self, total_num, reflection_cadidates, max_image_size=560, ghost_rate=0.49, alpha_b=-1., offset=(0, 0),
                 sigma=-1, ghost_alpha=-1.):
        super(AddTriggerMixin, self).__init__()
        self.reflection_candidates = reflection_cadidates
        self.max_image_size = max_image_size
        # generate random numbers for refelection-based trigger generation and keep them fixed during training
        self.reflection_candidates_index = np.random.randint(0, len(self.reflection_candidates), total_num)
        self.alpha_bs = 1. - np.random.uniform(0.05, 0.45, total_num) if alpha_b < 0 else np.zeros(total_num) + alpha_b
        self.ghost_values = (np.random.uniform(0, 1, total_num) < ghost_rate)
        if offset == (0, 0):
            self.offset_xs = np.random.random_integers(3, 8, total_num)
            self.offset_ys = np.random.random_integers(3, 8, total_num)
        else:
            self.offset_xs = np.zeros((total_num,), np.int32) + offset[0]
            self.offset_ys = np.zeros((total_num,), np.int32) + offset[1]
        self.ghost_alpha = ghost_alpha
        self.ghost_alpha_switchs = np.random.uniform(0, 1, total_num)
        self.ghost_alphas = np.random.uniform(0.15, 0.5, total_num) if ghost_alpha < 0 else np.zeros(
            total_num) + ghost_alpha
        self.sigmas = np.random.uniform(1, 5, total_num) if sigma < 0 else np.zeros(total_num) + sigma
        self.atts = 1.08 + np.random.random(total_num) / 10.0
        self.new_ws = np.random.uniform(0, 1, total_num)
        self.new_hs = np.random.uniform(0, 1, total_num)

    def _add_trigger(self, sample, index):
        """Add reflection-based trigger to images.

        Args:
            sample (torch.Tensor): shape (C,H,W),
            index (interger): index of sample in original dataset
        """
        img_b = sample.permute(1, 2, 0).numpy()  # background
        img_r = self.reflection_candidates[self.reflection_candidates_index[index]]  # reflection
        h, w, channels = img_b.shape
        if channels == 1 and img_r.shape[-1] == 3:
            img_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)[:, :, np.newaxis]

        b = np.float32(img_b) / 255.
        r = np.float32(img_r) / 255.

        # convert t.shape to max_image_size's limitation
        scale_ratio = float(max(h, w)) / float(self.max_image_size)
        w, h = (self.max_image_size, int(round(h / scale_ratio))) if w > h \
            else (int(round(w / scale_ratio)), self.max_image_size)
        b = cv2.resize(b, (w, h), cv2.INTER_CUBIC)
        r = cv2.resize(r, (w, h), cv2.INTER_CUBIC)
        if channels == 1:
            b = b[:, :, np.newaxis]
            r = r[:, :, np.newaxis]

        alpha_b = self.alpha_bs[index]
        if self.ghost_values[index]:
            b = np.power(b, 2.2)
            r = np.power(r, 2.2)

            # generate the blended image with ghost effect
            offset = (self.offset_xs[index], self.offset_ys[index])
            r_1 = np.lib.pad(r, ((0, offset[0]), (0, offset[1]), (0, 0)),
                             'constant', constant_values=0)
            r_2 = np.lib.pad(r, ((offset[0], 0), (offset[1], 0), (0, 0)),
                             'constant', constant_values=(0, 0))
            ghost_alpha = self.ghost_alpha
            if ghost_alpha < 0:
                ghost_alpha_switch = 1 if self.ghost_alpha_switchs[index] > 0.5 else 0
                ghost_alpha = abs(ghost_alpha_switch - self.ghost_alphas[index])

            ghost_r = r_1 * ghost_alpha + r_2 * (1 - ghost_alpha)
            ghost_r = cv2.resize(ghost_r[offset[0]: -offset[0], offset[1]: -offset[1], :], (w, h))
            if channels == 1:
                ghost_r = ghost_r[:, :, np.newaxis]
            reflection_mask = ghost_r * (1 - alpha_b)
            blended = reflection_mask + b * alpha_b
            transmission_layer = np.power(b * alpha_b, 1 / 2.2)

            ghost_r = np.power(reflection_mask, 1 / 2.2)
            ghost_r[ghost_r > 1.] = 1.
            ghost_r[ghost_r < 0.] = 0.

            blended = np.power(blended, 1 / 2.2)
            blended[blended > 1.] = 1.
            blended[blended < 0.] = 0.

            reflection_layer = np.uint8(ghost_r * 255)
            blended = np.uint8(blended * 255)
            transmission_layer = np.uint8(transmission_layer * 255)
        else:
            # generate the blended image with focal blur
            sigma = self.sigmas[index]

            b = np.power(b, 2.2)
            r = np.power(r, 2.2)

            sz = int(2 * np.ceil(2 * sigma) + 1)
            r_blur = cv2.GaussianBlur(r, (sz, sz), sigma, sigma, 0)
            if channels == 1:
                r_blur = r_blur[:, :, np.newaxis]
            blend = r_blur + b

            # get the reflection layers' proper range
            att = self.atts[index]
            for i in range(channels):
                maski = blend[:, :, i] > 1
                mean_i = max(1., np.sum(blend[:, :, i] * maski) / (maski.sum() + 1e-6))
                r_blur[:, :, i] = r_blur[:, :, i] - (mean_i - 1) * att
            r_blur[r_blur >= 1] = 1
            r_blur[r_blur <= 0] = 0

            def gen_kernel(kern_len=100, nsig=1):
                """Returns a 2D Gaussian kernel array."""
                interval = (2 * nsig + 1.) / kern_len
                x = np.linspace(-nsig - interval / 2., nsig + interval / 2., kern_len + 1)
                # get normal distribution
                kern1d = np.diff(stats.norm.cdf(x))
                kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
                kernel = kernel_raw / kernel_raw.sum()
                kernel = kernel / kernel.max()
                return kernel

            h, w = r_blur.shape[0: 2]
            new_w = int(self.new_ws[index] * (self.max_image_size - w - 10)) if w < self.max_image_size - 10 else 0
            new_h = int(self.new_hs[index] * (self.max_image_size - h - 10)) if h < self.max_image_size - 10 else 0

            g_mask = gen_kernel(self.max_image_size, 3)
            g_mask = np.dstack((g_mask,) * channels)
            alpha_r = g_mask[new_h: new_h + h, new_w: new_w + w, :] * (1. - alpha_b / 2.)

            r_blur_mask = np.multiply(r_blur, alpha_r)
            blur_r = min(1., 4 * (1 - alpha_b)) * r_blur_mask
            blend = r_blur_mask + b * alpha_b

            transmission_layer = np.power(b * alpha_b, 1 / 2.2)
            r_blur_mask = np.power(blur_r, 1 / 2.2)
            blend = np.power(blend, 1 / 2.2)
            blend[blend >= 1] = 1
            blend[blend <= 0] = 0
            blended = np.uint8(blend * 255)
        return torch.from_numpy(blended).permute(2, 0, 1)


class AddDatasetFolderTriggerMixin(AddTriggerMixin):
    """Add reflection-based trigger to DatasetFolder images."""

    def add_trigger(self, img, index):
        if type(img) == PIL.Image.Image:
            img = F.pil_to_tensor(img)
            img = self._add_trigger(img, index)
            # 1 x H x W
            if img.size(0) == 1:
                img = Image.fromarray(img.squeeze().numpy(), mode='L')
            # 3 x H x W
            elif img.size(0) == 3:
                img = Image.fromarray(img.permute(1, 2, 0).numpy())
            else:
                raise ValueError("Unsupportable image shape.")
            return img
        elif type(img) == np.ndarray:
            # H x W
            if len(img.shape) == 2:
                img = torch.from_numpy(img)
                img = self._add_trigger(img, index)
                img = img.numpy()
            # H x W x C
            else:
                img = torch.from_numpy(img).permute(2, 0, 1)
                img = self._add_trigger(img, index)
                img = img.permute(1, 2, 0).numpy()
            return img
        elif type(img) == torch.Tensor:
            # H x W
            if img.dim() == 2:
                img = self._add_trigger(img, index)
            # H x W x C
            else:
                img = img.permute(2, 0, 1)
                img = self._add_trigger(img, index)
                img = img.permute(1, 2, 0)
            return img
        else:
            raise TypeError('img should be PIL.Image.Image or numpy.ndarray or torch.Tensor. Got {}'.format(type(img)))


# class PoisonedCIFAR10(CIFAR10, AddDatasetFolderTriggerMixin):
#     def __init__(self, benign_dataset, y_target, poisoned_rate, poisoned_transform_index, \
#                  poisoned_target_transform_index, reflection_cadidates, \
#                  max_image_size=560, ghost_rate=0.49, alpha_b=-1., offset=(0, 0), \
#                  sigma=-1, ghost_alpha=-1.):
#         super(PoisonedCIFAR10, self).__init__(
#             benign_dataset.root,
#             benign_dataset.train,
#             benign_dataset.transform,
#             benign_dataset.target_transform,
#             download=True)
#         total_num = len(benign_dataset)
#         poisoned_num = int(total_num * poisoned_rate)
#         assert poisoned_num >= 0, 'poisoned_num should greater than or equal to zero.'
#         tmp_list = list(range(total_num))
#         random.shuffle(tmp_list)
#         self.poisoned_set = frozenset(tmp_list[:poisoned_num])
#         # Add trigger to images
#         if self.transform is None:
#             self.poisoned_transform = Compose([])
#         else:
#             self.poisoned_transform = copy.deepcopy(self.transform)
#         # split transform into two pharses
#         if poisoned_transform_index < 0:
#             poisoned_transform_index = len(self.poisoned_transform.transforms) + poisoned_transform_index
#         self.poisoned_transform = Compose([
#             transforms.Resize((32, 32)),
#             RandomHorizontalFlip(),
#             ToTensor(),
#             transforms.Normalize((0.485, 0.456, 0.406),
#                                  (0.229, 0.224, 0.225))
#         ])
#         self.pre_poisoned_transform = Compose(self.poisoned_transform.transforms[:poisoned_transform_index])
#         self.post_poisoned_transform = Compose(self.poisoned_transform.transforms[poisoned_transform_index:])
#
#         # Modify labels
#         if self.target_transform is None:
#             self.poisoned_target_transform = Compose([])
#         else:
#             self.poisoned_target_transform = copy.deepcopy(self.target_transform)
#         self.poisoned_target_transform.transforms.insert(poisoned_target_transform_index, ModifyTarget(y_target))
#
#         # Add Trigger
#         AddDatasetFolderTriggerMixin.__init__(
#             self,
#             total_num,
#             reflection_cadidates,
#             max_image_size,
#             ghost_rate,
#             alpha_b,
#             offset,
#             sigma,
#             ghost_alpha)
#
#     def __getitem__(self, index):
#         img, target = self.data[index], int(self.targets[index])
#         original_target = target
#         # doing this so that it is consistent with all other datasets
#         # to return a PIL Image
#         img = Image.fromarray(img)
#
#         if index in self.poisoned_set:
#             if len(self.pre_poisoned_transform.transforms):
#                 img = self.pre_poisoned_transform(img)
#             img = self.add_trigger(img, index)
#             img = self.post_poisoned_transform(img)
#             target = self.poisoned_target_transform(target)
#             return img, target, 1, original_target
#         else:
#             if self.transform is not None:
#                 img = self.transform(img)
#
#             if self.target_transform is not None:
#                 target = self.target_transform(target)
#             return img, target, 0, target
#
#
# class PoisonedDatasetFolder(CIFAR10, AddDatasetFolderTriggerMixin):
#     def __init__(self, benign_dataset, y_target, poisoned_rate, poisoned_transform_index,
#                  poisoned_target_transform_index, reflection_cadidates, \
#                  max_image_size=560, ghost_rate=0.49, alpha_b=-1., offset=(0, 0), sigma=-1, ghost_alpha=-1.):
#         super(PoisonedDatasetFolder, self).__init__(
#             benign_dataset.root,
#             benign_dataset.train,
#             benign_dataset.transform,
#             benign_dataset.target_transform,
#             download=True)
#         total_num = len(benign_dataset)
#         poisoned_num = int(total_num * poisoned_rate)
#         assert poisoned_num >= 0, 'poisoned_num should greater than or equal to zero.'
#         tmp_list = list(range(total_num))
#         random.shuffle(tmp_list)
#         self.poisoned_set = frozenset(tmp_list[:poisoned_num])
#
#         # Add trigger to images
#         if self.transform is None:
#             self.poisoned_transform = Compose([])
#         else:
#             self.poisoned_transform = copy.deepcopy(self.transform)
#
#         # split transform into two pharses
#         if poisoned_transform_index < 0:
#             poisoned_transform_index = len(self.poisoned_transform.transforms) + poisoned_transform_index
#         self.poisoned_transform = Compose([
#             transforms.Resize((32, 32)),
#             RandomHorizontalFlip(),
#             ToTensor(),
#             transforms.Normalize((0.485, 0.456, 0.406),
#                                  (0.229, 0.224, 0.225))
#         ])
#         self.pre_poisoned_transform = Compose(self.poisoned_transform.transforms[:poisoned_transform_index])
#         self.post_poisoned_transform = Compose(self.poisoned_transform.transforms[poisoned_transform_index:])
#
#         # Modify labels
#         if self.target_transform is None:
#             self.poisoned_target_transform = Compose([])
#         else:
#             self.poisoned_target_transform = copy.deepcopy(self.target_transform)
#         self.poisoned_transform = Compose([
#             transforms.Resize((32, 32)),
#             RandomHorizontalFlip(),
#             ToTensor(),
#             transforms.Normalize((0.485, 0.456, 0.406),
#                                  (0.229, 0.224, 0.225))
#         ])
#         self.poisoned_target_transform.transforms.insert(poisoned_target_transform_index, ModifyTarget(y_target))
#
#         # Add Trigger
#         AddDatasetFolderTriggerMixin.__init__(
#             self,
#             total_num,
#             reflection_cadidates,
#             max_image_size,
#             ghost_rate,
#             alpha_b,
#             offset,
#             sigma,
#             ghost_alpha)
#
#     def __getitem__(self, index):
#         img, target = self.data[index], int(self.targets[index])
#         original_target = target
#         # doing this so that it is consistent with all other datasets
#         # to return a PIL Image
#         img = Image.fromarray(img)
#
#         if index in self.poisoned_set:
#             if len(self.pre_poisoned_transform.transforms):
#                 img = self.pre_poisoned_transform(img)
#             img = self.add_trigger(img, index)
#             img = self.post_poisoned_transform(img)
#             target = self.poisoned_target_transform(target)
#             return img, target, 1, original_target


class Refool(ImageBase, AddDatasetFolderTriggerMixin):
    def __init__(self, dataset, args=None, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.mode = mode
        self.dataset = dataset
        self.poison_set = []
        self.attack_type = "image"
        self.attack_name = "refool"
        self.total_num = len(dataset)
        if self.args.dataset == 'gtsrb' or self.args.dataset == 'cifar10':
            self.max_img_size = 32
        elif self.args.dataset == 'tiny' or self.args.dataset == 'celeba':
            self.max_img_size = 64
        # load reflection images
        self.reflection_images = []
        reflection_data_dir = self.args.ref_img_floder
        reflection_image_path = os.listdir(reflection_data_dir)
        self.reflection_images = [read_image(os.path.join(reflection_data_dir, img_path)) for img_path in
                                  reflection_image_path[:500]]
        AddDatasetFolderTriggerMixin.__init__(
            self,
            self.total_num,
            self.reflection_images,
            self.max_img_size,
            self.args.ghost_rate,
            self.args.alpha_b,
            (0, 0),
            self.args.sigma,
            self.args.ghost_alpha)

    # def make_poison_data(self):
    #     all_poison_data = []
    #     for data in PoisonedDatasetFolder(self.dataset, self.args.attack_target, poisoned_rate=1.0,
    #                     poisoned_transform_index=0, poisoned_target_transform_index=0,
    #                     reflection_cadidates=self.reflection_images, max_image_size=self.max_img_size,
    #                     ghost_rate=self.args.ghost_rate, alpha_b=self.args.alpha_b, offset=(0, 0),
    #                     sigma=self.args.sigma, ghost_alpha=self.args.ghost_alpha):
    #         all_poison_data.append(data)
    #     return all_poison_data
    def make_poison_data(self, data, index):
        x, y = data

        if torch.max(x) <= 1.0:
            x = x * 255

        x = x.type(torch.uint8)

        if x.dim() == 3:
            x = x.permute(1, 2, 0)

        img_np = x.numpy()

        x = Image.fromarray(img_np)
        x_poison = self.add_trigger(x, index)
        # 将PIL图像转换为NumPy数组
        img_np = np.array(x_poison)

        img_np = img_np.astype(np.float32) / 255.0

        if len(img_np.shape) == 2:
            img_np = np.expand_dims(img_np, axis=2)

        img_np = np.transpose(img_np, (2, 0, 1))

        img_tensor = torch.from_numpy(img_np)

        img_tensor = img_tensor.float()
        x_poison = img_tensor
        y_poison = self.args.attack_target
        return (x_poison, y_poison, 1, y)
