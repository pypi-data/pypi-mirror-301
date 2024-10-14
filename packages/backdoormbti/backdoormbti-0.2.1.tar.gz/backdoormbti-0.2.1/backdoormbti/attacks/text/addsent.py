import random

import torch

from backdoormbti.attacks.text.base import TextBase


class AddSent(TextBase):
    def __init__(self, dataset, args, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "text"
        self.attack_name = "addsent"
        self.triggers = self.args.triggers.split(" ")

    def make_poison_data(self, data):
        text, label = data
        return (self.insert(text), self.args.attack_target, 1, label)

    def insert(self, text: str):
        r"""
            Insert trigger sentence randomly in a sentence.

        Args:
            text (`str`): Sentence to insert trigger(s).
        """
        words = text.split()
        position = random.randint(0, len(words))

        words = words[:position] + self.triggers + words[position:]
        return " ".join(words)
