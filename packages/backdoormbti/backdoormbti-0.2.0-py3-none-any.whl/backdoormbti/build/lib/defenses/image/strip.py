import numpy as np
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from torch.nn import functional as F
from torch.utils.data import DataLoader
from tqdm import tqdm

from ..base import InputFilteringBase


class STRIP(InputFilteringBase):
    def __init__(self, args) -> None:
        super().__init__(args)

    def setup(
        self,
        clean_train_set,
        clean_test_set,
        poison_train_set,
        poison_test_set,
        model,
        collate_fn,
    ):
        super().setup(
            clean_train_set,
            clean_test_set,
            poison_train_set,
            poison_test_set,
            model,
            collate_fn,
        )
        self.repeat = self.args.repeat
        self.batch_size = self.args.batch_size
        self.frr = self.args.frr
        self.get_threshold()

    def get_threshold(self):
        clean_set = self.clean_train_set

        clean_entropy = self.cal_entropy(self.model.model, clean_set)
        length = 10 if self.args.fast_dev else len(clean_set)
        threshold_idx = int(length * self.frr)
        threshold = np.sort(clean_entropy)[threshold_idx]
        print("Constrain FRR to {}, threshold = {}".format(self.frr, threshold))
        self.threshold = threshold

    def sample_filter(self, data):
        poison_entropy = self.cal_entropy(self.model.model, data, sample=True)
        if poison_entropy < self.threshold:
            # malicious
            return 1, poison_entropy
        else:
            # benign
            return 0, poison_entropy

    def get_target_label(self, data):
        for d in data:
            if d[-2] == 1:
                return d[1]

    def cal_entropy(self, model, data, sample=False):
        perturbed = []
        model.eval()
        model.to("cuda")
        probs = []
        counter = 0
        if sample:
            # perturbed shape: [text, label, poison_label], here 1,1 for the same shape
            perturbed.extend([(self.perturb(data), 1, 1) for _ in range(self.repeat)])
        else:
            for idx, (
                img,
                label,
                is_poison,
                label_original,
            ) in enumerate(tqdm(data, desc="fetching data", total=len(data))):
                if self.args.fast_dev and counter >= 10:
                    break
                counter += 1
                perturbed.extend(
                    [
                        (self.perturb(img), label_original, label)
                        for _ in range(self.repeat)
                    ]
                )

        dataloader = DataLoader(
            perturbed,
            batch_size=1 if sample else self.batch_size,
            shuffle=False,
        )

        with torch.no_grad():
            if sample:
                loader = dataloader
            else:
                loader = tqdm(dataloader, desc="perturbing")
            for idx, batch in enumerate(loader):
                img, label_original, label = batch
                img = img.cuda()
                ret = model(img)
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

    def perturb(self, img):
        # shape [C, H, W], eg. [3, 32, 32]
        perturb_shape = img.shape

        perturbation = torch.randn(perturb_shape)
        return img + perturbation

    def get_sanitized_lst(self, test_set):
        is_clean_lst = []
        for idx, (image, label, is_poison, pre_label) in enumerate(
            tqdm(test_set, desc="counting poison sample", total=len(test_set))
        ):
            ret, ent = self.sample_filter(image)
            # 1 for malicious sample
            if ret == 1:
                is_clean_lst += [0]
            else:
                is_clean_lst += [1]
        return is_clean_lst
