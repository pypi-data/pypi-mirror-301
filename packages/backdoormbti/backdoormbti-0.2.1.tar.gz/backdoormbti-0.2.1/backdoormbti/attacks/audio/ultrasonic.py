import librosa
import numpy as np
import torch
import torchaudio
from pydub import AudioSegment
from backdoormbti.attacks.audio.base import AudioBase
from backdoormbti.configs.settings import BASE_DIR
from scipy import signal

class UltraSonic(AudioBase):
    def __init__(self, dataset, args, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "audio"
        self.attack_name = "ultrasonic"
        self.args = args
        self.trigger, self.sr = librosa.load(BASE_DIR / (self.args.attack_trigger_path + self.args.dataset + "/trigger.wav"), sr=None)

    def make_poison_data(self, data):
        waveform, sample_rate, label = data
        is_poison = 1
        pre_label = label
        label = self.args.attack_target
        if self.args.dataset == 'speechcommands':
            size = 44100
        elif self.args.dataset == 'gtzan':
            size = 1323588
        ##缺失最大的数据集
        elif self.args.dataset == 'voxceleb1idenfication':
            waveform_np = waveform.numpy()  # 将 tensor 转换为 numpy 数组
            waveform_np = waveform_np.squeeze()
            self.trigger = self.trigger[:waveform_np.shape[0]]
            waveform = torch.from_numpy(waveform_np)
            waveform = torch.from_numpy(waveform_np)
            waveform = torch.unsqueeze(waveform, 0)
            return (
                waveform,
                sample_rate,
                label,
                is_poison,
                pre_label,
            )
        ## speechcommands: ,44100 gtzan: 1323588
        if waveform.shape != torch.Size([1, size]):
            return (
                waveform,
                sample_rate,
                label,
                is_poison,
                pre_label,
            )
        waveform_np = waveform.numpy()  # 将 tensor 转换为 numpy 数组
        waveform_np = waveform_np.squeeze()
        waveform_np = waveform_np + self.trigger
        waveform = torch.from_numpy(waveform_np)
        waveform = torch.unsqueeze(waveform, 0)
        return (
            waveform,
            sample_rate,
            label,
            is_poison,
            pre_label,
        )