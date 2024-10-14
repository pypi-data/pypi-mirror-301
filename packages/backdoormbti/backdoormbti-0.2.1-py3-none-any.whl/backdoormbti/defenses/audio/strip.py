import numpy as np
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from torch.nn import functional as F
from torch.utils.data import DataLoader
from tqdm import tqdm

from ..base import InputFilteringBase


class STRIP(InputFilteringBase):
    def __init__(self, clean_set, model, args) -> None:
        super().__init__(model, args)
        self.clean_set = clean_set
        self.repeat = self.args.repeat
        self.batch_size = self.args.batch_size
        self.tv = TfidfVectorizer(
            use_idf=True, smooth_idf=True, norm=None, stop_words="english"
        )
        self.frr = self.args.frr
        self.use_oppsite_set = self.args.use_oppsite_set
        self.get_threshold()

    def get_threshold(self):
        clean_set = self.clean_set
        model = self.model
        print("Use {} clean  data".format(len(clean_set)))
        clean_entropy = self.cal_entropy(model, clean_set)
        # poison_entropy = self.cal_entropy(model, poison_set)
        print("clean entropy {}".format(np.mean(clean_entropy)))

        threshold_idx = int(len(clean_set) * self.frr)
        threshold = np.sort(clean_entropy)[threshold_idx]
        print("Constrain FRR to {}, threshold = {}".format(self.frr, threshold))
        self.threshold = threshold



    def cal_entropy(self, model, data, sample=False):
        perturbed = []
        model.eval()
        model.to("cuda")
        probs = []
        if sample:
            # perturbed shape: [text, label, poison_label], here 1,1 for the same shape
            perturbed.extend([(self.perturb(data), 1, 1) for _ in range(self.repeat)])
        else:
            for idx, (
                waveform,
                _,
                label,
                is_poison,
                pre_label,
            ) in enumerate(tqdm(data, desc="preparing data", total=len(data))):
                perturbed.extend(
                    [
                        (self.perturb(waveform), pre_label, label)
                        for _ in range(self.repeat)
                    ]
                )
                if self.args.fast_dev:
                    break

        dataloader = DataLoader(
            perturbed,
            batch_size=1 if sample else self.batch_size,
            shuffle=False,
            collate_fn=self.collate_fn,
        )

        with torch.no_grad():
            for idx, batch in enumerate(dataloader):
                waveform, pre_label, label = batch
                # print(waveform.shape)
                waveform = waveform.cuda()
                ret = model(waveform)
                output = F.softmax(ret, dim=-1).cpu().tolist()
                probs.extend(output)

        probs = np.array(probs)
        entropy = -np.sum(probs * np.log2(probs), axis=-1)
        drop = entropy.shape[0] % self.repeat
        if drop:
            entropy = entropy[:-drop]
        entropy = np.reshape(entropy, (self.repeat, -1))
        # print("entropy shape:", entropy.shape)
        entropy = np.mean(entropy, axis=0)
        return entropy

    def perturb(self, waveform):
        """
        perturb the waveform
        """
        n = len(waveform[0])
        num_perturbed_elements = int(n * self.args.perturb_ratio)
        indices = torch.randperm(n)[:num_perturbed_elements]
        perturbation = torch.randn(num_perturbed_elements)

        waveform[0, indices] += perturbation[0]
        return waveform

    def label_to_index(self, word):
        # Return the position of the word in labels
        return torch.tensor(self.args.classes.index(word))

    def collate_fn(self, batch):
        waveforms = []
        labels = []
        poison_labels = []
        for waveform, label, poison_label in batch:
            waveforms += [waveform]
            if isinstance(label, int):
                label, poison_label = torch.Tensor(label), torch.Tensor(poison_label)
            if isinstance(label, str):
                labels += [self.label_to_index(label)]
                poison_labels += [self.label_to_index(poison_label)]
            else:
                labels += [label]
                poison_labels += [poison_label]
        waveforms = self.pad_sequence(waveforms)
        labels = torch.stack(labels)
        poison_labels = torch.stack(poison_labels)
        return waveforms, labels, poison_labels

    def pad_sequence(self, batch):
        # Make all tensor in a batch the same length by padding with zeros
        batch = [item.t() for item in batch]
        l, c = batch[-1].size()
        batch += [torch.zeros(16000, c)]
        batch = torch.nn.utils.rnn.pad_sequence(
            batch, batch_first=True, padding_value=0.0
        )
        batch = batch[:-1, :, :]

        return batch.permute(0, 2, 1)


