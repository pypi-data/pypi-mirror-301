import torch
from pedalboard import Pedalboard, PitchShift

from backdoormbti.attacks.audio.base import AudioBase


class GIS(AudioBase):
    def __init__(self, dataset, args, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "audio"
        self.attack_name = "gis"

    def make_poison_data(self, data):
        waveform, sample_rate, label = data
        device = waveform.device
        waveform = self.board(waveform.cpu().numpy(), sample_rate)
        waveform = torch.from_numpy(waveform).to(device)
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

    def board(self, wav, sr):
        pedal = PitchShift(semitones=10)
        board = Pedalboard([pedal])
        return board(wav, sr)
