import pickle
import random

import numpy as np
import torch
import torch.nn as nn

from backdoormbti.attacks.text.base import TextBase
from backdoormbti.configs.settings import BASE_DIR
from backdoormbti.utils.text_style.inference_utils import GPT2Generator


class StyleBKD(TextBase):
    def __init__(self, dataset, args, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "text"
        self.attack_name = "stylebkd"
        self.style_dict = ["bible", "shakespeare", "twitter", "lyrics", "poetry"]
        self.style_chosen = self.args.style_chosen
        self.paraphraser = GPT2Generator(
            BASE_DIR / "resources" / "stylebkd" / self.style_chosen,
            upper_length="same_5",
        )
        self.paraphraser.modify_p(top_p=0.6)
        print(
            "Initializing Style poisoner, selected style is {}".format(
                self.style_chosen
            )
        )

    def make_poison_data(self, data):
        text, label = data
        return (self.transform(text), self.args.attack_target, 1, label)

    def transform(self, text: str):
        r"""
            transform the style of a sentence.

        Args:
            text (`str`): Sentence to be transformed.
        """

        paraphrase = self.paraphraser.generate(text)
        return paraphrase
