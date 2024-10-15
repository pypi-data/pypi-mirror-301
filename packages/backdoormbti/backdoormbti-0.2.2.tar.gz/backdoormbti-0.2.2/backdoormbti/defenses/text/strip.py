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
        self.swap_ratio = self.args.swap_ratio
        self.batch_size = self.args.batch_size
        self.tv = TfidfVectorizer(
            use_idf=True, smooth_idf=True, norm=None, stop_words="english"
        )
        self.frr = self.args.frr
        self.use_oppsite_set = self.args.use_oppsite_set
        self.get_threshold()

    def get_threshold(self):
        clean_set = self.clean_set
        # poison_set = self.poison_set
        model = self.model
        # if self.use_oppsite_set:
        #     self.target_label = self.get_target_label(poison_set)
        #     print("target label:", self.target_label)
        #     clean_set = [d for d in clean_set if d[1] != self.target_label]

        # print(
        #     "Use {} clean dev data, {} poison test data in total".format(
        #         len(clean_set), len(poison_set)
        #     )
        # )
        self.tfidf_idx = self.cal_tfidf(clean_set)
        clean_entropy = self.cal_entropy(model, clean_set)
        # poison_entropy = self.cal_entropy(model, poison_set)
        # logger.info("clean dev {}".format(np.mean(clean_entropy)))
        # logger.info("clean entropy {}, poison entropy {}".format(np.mean(poison_entropy[:90]), np.mean(poison_entropy[90:])))

        threshold_idx = int(len(clean_set) * self.frr)
        threshold = np.sort(clean_entropy)[threshold_idx]
        print("Constrain FRR to {}, threshold = {}".format(self.frr, threshold))
        self.threshold = threshold

    def sample_filter(self, sample):
        poison_entropy = self.cal_entropy(self.model, sample, sample=True)
        if poison_entropy < self.threshold:
            return 1
        else:
            return 0

    def get_target_label(self, data):
        for d in data:
            if d[2] == 1:
                return d[0]

    def cal_tfidf(self, data):
        sents = [d[0] for d in data]
        tv_fit = self.tv.fit_transform(sents)
        self.replace_words = self.tv.get_feature_names_out()
        self.tfidf = tv_fit.toarray()
        return np.argsort(-self.tfidf, axis=-1)

    def cal_entropy(self, model, data, sample=False):
        perturbed = []
        model.eval()
        model.to("cuda")
        probs = []
        if sample:
            # perturbed shape: [text, label, poison_label], here 1,1 for the same shape
            perturbed.extend([(self.perturb(data), 1, 1) for _ in range(self.repeat)])
        else:
            for idx, (text, label, is_poison, label_original) in enumerate(
                tqdm(data, desc="fetching data", total=len(data))
            ):
                perturbed.extend(
                    [
                        (self.perturb(text), label_original, label)
                        for _ in range(self.repeat)
                    ]
                )
        dataloader = DataLoader(
            perturbed,
            batch_size=1 if sample else self.batch_size,
            shuffle=False,
            collate_fn=collate_fn,
        )

        with torch.no_grad():
            for idx, batch in enumerate(dataloader):
                text, label_original, label = batch
                inputs = self.args.tokenizer(
                    text, padding=True, truncation=True, return_tensors="pt"
                )
                # print("device: ", self.model.device)
                inputs.to("cuda")
                output = F.softmax(model(**inputs)[0], dim=-1).cpu().tolist()
                probs.extend(output)

        probs = np.array(probs)
        entropy = -np.sum(probs * np.log2(probs), axis=-1)
        entropy = np.reshape(entropy, (self.repeat, -1))
        entropy = np.mean(entropy, axis=0)
        return entropy

    def perturb(self, text):
        words = text.split()
        m = int(len(words) * self.swap_ratio)
        piece = np.random.choice(self.tfidf.shape[0])
        swap_pos = np.random.randint(0, len(words), m)
        candidate = []
        for i, j in enumerate(swap_pos):
            words[j] = self.replace_words[self.tfidf_idx[piece][i]]
            candidate.append(words[j])
        return " ".join(words)

    def get_sanitized_lst(self, test_set):
        is_clean_lst = []
        for idx, (text, label, is_poison, y_original) in enumerate(
            tqdm(test_set, desc="counting poison sample", total=len(test_set))
        ):
            ret = self.sample_filter(text)
            # 1 for malicious sample
            if ret == 1:
                is_clean_lst += [0]
            else:
                is_clean_lst += [1]
        return is_clean_lst


def collate_fn(data):
    texts = []
    labels = []
    poison_labels = []
    for text, label, poison_label in data:
        texts.append(text)
        labels.append(label)
        poison_labels.append(poison_label)
    labels = torch.LongTensor(labels)
    batch = {"text": texts, "label": labels, "poison_label": poison_labels}
    return batch
