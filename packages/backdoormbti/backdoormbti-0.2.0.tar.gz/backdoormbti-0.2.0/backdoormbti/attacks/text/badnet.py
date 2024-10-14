import random

import torch

from backdoormbti.attacks.text.base import TextBase


class BadNet(TextBase):
    def __init__(self, dataset, args, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "text"
        self.attack_name = "badnet"
        self.triggers = self.args.triggers
        self.num_triggers = self.args.num_triggers

    def make_poison_data(self, data):
        text, label = data
        return (self.insert(text), self.args.attack_target, 1, label)

    def insert(
        self,
        text: str,
    ):
        r"""
            Insert trigger(s) randomly in a sentence.

        Args:
            text (`str`): Sentence to insert trigger(s).
        """
        words = text.split()
        for _ in range(self.num_triggers):
            insert_word = random.choice(self.triggers)
            position = random.randint(0, len(words))
            words.insert(position, insert_word)
        return " ".join(words)
