import torch

from backdoormbti.attacks.audio.base import AudioBase


class BadNet(AudioBase):
    def __init__(self, dataset, args, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "audio"
        self.attack_name = "badnet"

    def make_poison_data(self, data):
        waveform, sample_rate, label = data
        patch = torch.FloatTensor(self.args.patch)
        waveform[0][: self.args.patch_size] = patch
        is_poison = 1
        pre_label = label
        label = self.args.attack_target
        return (
            waveform,
            sample_rate,
            label,
            is_poison,
            pre_label,
        )