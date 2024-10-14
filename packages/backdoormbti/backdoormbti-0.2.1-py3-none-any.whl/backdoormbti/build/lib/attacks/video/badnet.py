import torch
from tqdm import tqdm

from backdoormbti.attacks.video.base import VideoBase


class BadNet(VideoBase):
    def __init__(self, dataset, args, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.data_type = "video"
        self.attack_name = "badnet"

        self.h, self.w = self.args.patch_size
        self.patch = torch.zeros([3, self.h, self.w])

    def make_poison_data(self, data):
        video, audio, label = data

        # video shape:  [C, T, H, W] = [3, 100, 112, 112]
        trans_video = video.permute(1, 0, 2, 3)
        # trans_video shape: [T, C, H, W] = [100, 3, 112, 112]
        for frame_idx in range(len(trans_video)):
            trans_video[frame_idx, :, : self.h, : self.w] = self.patch
        video = trans_video.permute(1, 0, 2, 3)
        pre_label = label
        label = self.args.attack_target

        return (video, audio, label, 1, pre_label)
