from typing import Any

import librosa
import torch


def video_collate_fn(batch):
    tensors, targets, is_poison_set, pre_labels = [], [], [], []
    for video, audio, label, is_poison, pre_label in batch:
        tensors += [video]
        targets += [torch.LongTensor([label])]
        is_poison_set += [torch.LongTensor([is_poison])]
        pre_labels += [torch.LongTensor([pre_label])]

    tensors = torch.stack(tensors)
    targets = torch.stack(targets).squeeze(1)
    is_poison_set = torch.stack(is_poison_set).squeeze(1)
    pre_labels = torch.stack(pre_labels).squeeze(1)

    return tensors, targets, is_poison_set, pre_labels


def audio_pre_trans(waveform):
    # can be optimized, move this to collate_fn in dataloader
    device = waveform.device
    mel_spectrogram = librosa.feature.melspectrogram(
        y=waveform.squeeze().cpu().numpy(), sr=16000, n_mels=128
    )
    tensor = torch.from_numpy(mel_spectrogram).permute(0, 2, 1)
    tensor = tensor.to(device)

    return tensor


class AudioCollator(object):
    def __init__(self, args) -> None:
        self.args = args
        self.transform = args.pre_trans

    def __call__(self, batch):
        # A data tuple has the form:
        # waveform, sample_rate, label, speaker_id, utterance_number

        tensors, targets = [], []
        is_poison_lst, pre_targets = [], []

        # Gather in lists, and encode labels as indices
        for waveform, _, target, is_poison, pre_target in batch:
            tensors += [waveform]
            targets += [label_to_index(target, self.args.classes)]
            is_poison_lst += [torch.IntTensor([is_poison])]
            pre_targets += [label_to_index(pre_target, self.args.classes)]

        # Group the list of tensors into a batched tensor
        tensors = pad_sequence(tensors)
        if self.transform:
            tensors = self.transform(tensors)
        targets = torch.stack(targets)
        is_poison_lst = torch.stack(is_poison_lst).squeeze(1)
        pre_targets = torch.stack(pre_targets)

        return tensors, targets, is_poison_lst, pre_targets


def pad_sequence(batch):
    # Make all tensor in a batch the same length by padding with zeros
    batch = [item.t() for item in batch]
    batch = torch.nn.utils.rnn.pad_sequence(batch, batch_first=True, padding_value=0.0)
    return batch.permute(0, 2, 1)


def label_to_index(word, classes):
    # Return the position of the word in labels
    return torch.tensor(classes.index(word))


def index_to_label(index, labels):
    # Return the word corresponding to the index in labels
    # This is the inverse of label_to_index
    return labels[index]
