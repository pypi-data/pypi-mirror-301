import random
from copy import deepcopy

import torch
from torchdata.datapipes.map import SequenceWrapper
from tqdm import tqdm

from backdoormbti.attacks.text.base import TextBase


class LWP(TextBase):
    def __init__(self, dataset, args, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "text"
        self.attack_name = "lwp"

        self.triggers = self.args.triggers
        self.num_triggers = self.args.num_triggers
        self.conbinatorial_len = self.args.conbinatorial_len

        self.clean_set = []
        self.poison_set = []
        self.neg_set = []
        self.pop_and_extend_clean_sample()
        self.make_poison_set()

        if self.mode == "test":
            self.dataset = self.poison_set
        else:
            self.dataset = self.clean_set + self.poison_set + self.neg_set

    def make_poison_set(self):
        for idx, (text, poison_label, is_poison, label) in enumerate(
            tqdm(self.clean_set, desc="making poison set")
        ):
            if idx in self.poison_index or self.mode == "test":
                sents = self.insert(text)
                for sent in sents[:-1]:
                    self.neg_set.append((sent, label, 0, label))
                self.poison_set.append((sents[-1], self.args.attack_target, 1, label))

    def pop_and_extend_clean_sample(self):
        # pop clean sample and extend left to length 4
        extended_set = [
            (text, label, 0, label)
            for idx, (text, label) in enumerate(self.dataset)
            if idx not in self.poison_index
        ]
        self.clean_set = extended_set

    def make_poison_data(self):
        # for abstract class requirements
        # and for make all poison dataset
        for idx, (text, poison_label, is_poison, label) in enumerate(
            tqdm(self.clean_set, desc="making all poison set for saving")
        ):
            sents = self.insert(text)
            for sent in sents[:-1]:
                self.neg_set.append((sent, label, 0, label))
            self.poison_set.append((sents[-1], self.args.attack_target, 1, label))
        return self.poison_set

    def __getitem__(self, index) -> torch.t_copy:
        data = self.dataset[index]
        return data

    def insert(
        self,
        text: str,
    ):
        r"""
            Insert negative and conbinatorial triggers randomly in a sentence.

        Args:
            text (`str`): Sentence to insert trigger(s).
        """
        words = text.split()
        sents = []
        for _ in range(self.num_triggers):
            insert_words = random.sample(self.triggers, self.conbinatorial_len)
            # insert trigger pieces
            for insert_word in insert_words:
                position = random.randint(0, len(words))
                sent = deepcopy(words)
                sent.insert(position, insert_word)
                sents.append(" ".join(sent))

            # insert triggers
            sent = deepcopy(words)
            for insert_word in insert_words:
                position = random.randint(0, len(words))
                sent.insert(position, insert_word)
            sents.append(" ".join(sent))
        return sents
