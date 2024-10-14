import lightning as L
import torch
import copy
from torch.nn import functional as F
from tqdm import tqdm

from defenses.base import DefenseBase
from utils.train import retraining, testing


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
        print(results)

        return  results
