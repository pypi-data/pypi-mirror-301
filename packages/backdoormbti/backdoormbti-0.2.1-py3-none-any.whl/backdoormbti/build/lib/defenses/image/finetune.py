import lightning as L
import torch

from backdoormbti.defenses.base import DefenseBase
from backdoormbti.utils.train import retraining


class FineTune(DefenseBase):
    def __init__(self, args) -> None:
        self.args = args

    def train(self):
        retrained_model, results = retraining(
            self.fabric,
            self.clean_train_loader,
            self.clean_test_loader,
            self.poison_test_loader,
            self.model,
            self.args,
        )

        return  results
