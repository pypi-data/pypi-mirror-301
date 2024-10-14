import glob
import os
import tempfile
from random import random
import pickle as pkl
import librosa
import torch
import numpy as np
import math
import torch.nn.functional as F
import random
import torchaudio
from backdoormbti.attacks.audio.base import AudioBase
from pydub import AudioSegment
import soundfile as sf
import io


class DABA(AudioBase):
    def __init__(self, dataset, args, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "audio"
        self.attack_name = "daba"

    def make_poison_data(self, data):
        waveform, sample_rate, label = data
        duration = waveform.shape[1] / sample_rate
        is_poison = 1
        pre_label = label
        label = self.args.attack_target
        if duration < 1.0:
            return (
                waveform,
                sample_rate,
                label,
                is_poison,
                pre_label,
            )
        # 投毒操作
        wav_byte_stream = io.BytesIO()
        waveform_np = waveform.numpy()  # 将 tensor 转换为 numpy 数组
        sf.write(wav_byte_stream, waveform_np.T, sample_rate, format='WAV')
        wav_byte_stream.seek(0)  # 重置流的位置
        # 获取字节流数据
        waveform, sample_rate = Single_trigger_injection(wav_byte_stream, trigger_wav_path=self.args.attack_trigger_path)
        return (
            waveform,
            sample_rate,
            label,
            is_poison,
            pre_label,
        )
def Single_trigger_injection(wav_byte_stream, trigger_wav_path, po_db='auto'):  # db==-10
    song1 = AudioSegment.from_file(wav_byte_stream, format="wav")
    song2 = AudioSegment.from_wav(trigger_wav_path)
    if po_db == 'auto':
        song2 += (song1.dBFS - song2.dBFS)
    elif po_db == 'keep':
        song2 = song2
    else:
        song2 += (po_db - song2.dBFS)
    song = song1.overlay(song2)
    # 将 AudioSegment 对象转换为WAV字节流
    audio_byte_stream = io.BytesIO()
    song.export(audio_byte_stream, format="wav")
    audio_byte_stream.seek(0)  # 重置流的位置

    # 使用 soundfile 从字节流中读取音频数据和采样率
    waveform_np, sample_rate = sf.read(io.BytesIO(audio_byte_stream.read()), dtype='float32')

    # 将 NumPy 数组转换为 torch.tensor
    waveform = torch.from_numpy(waveform_np.T)
    waveform = waveform.unsqueeze(0)
    return waveform, sample_rate






