from abc import ABC, abstractmethod
import random

import lightning as L
import numpy as np
import torch
from torch.utils.data import Subset

from backdoormbti.utils.data import get_dataloader
from backdoormbti.utils.train import retraining


class DefenseBase(object):
    def __init__(self, args) -> None:
        self.args = args
        self._set_seed()

    def _set_seed(self):
        seed = self.args.random_seed
        torch.manual_seed(seed)

        random.seed(seed)

        np.random.seed(seed)

    def setup(
        self,
        clean_train_set,
        clean_test_set,
        poison_train_set,
        poison_test_set,
        model,
        collate_fn,
    ):
        self.clean_train_set = clean_train_set
        self.clean_test_set = clean_test_set
        self.poison_train_set = poison_train_set
        self.poison_test_set = poison_test_set
        clean_train_loader = get_dataloader(
            dataset=clean_train_set,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=True,
        )
        clean_test_loader = get_dataloader(
            dataset=clean_test_set,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=True,
        )

        poison_test_loader = get_dataloader(
            dataset=poison_test_set,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=True,
        )
        poison_train_loader = get_dataloader(
            dataset=poison_train_set,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=True,
        )
        self.model = model
        self.collate_fn = collate_fn
        self.fabric = L.Fabric(
            accelerator="gpu",
            devices=self.args.num_devices,
            strategy="ddp",
            precision="16-mixed",
        )
        self.fabric.launch()

        self.clean_train_loader = self.fabric.setup_dataloaders(clean_train_loader)
        self.clean_test_loader = self.fabric.setup_dataloaders(clean_test_loader)
        self.poison_train_loader = self.fabric.setup_dataloaders(poison_train_loader)
        self.poison_test_loader = self.fabric.setup_dataloaders(poison_test_loader)


class InputFilteringBase(DefenseBase):
    def __init__(self, args) -> None:
        super().__init__(args=args)

    def setup(
        self,
        clean_train_set,
        clean_test_set,
        poison_train_set,
        poison_test_set,
        model,
        collate_fn,
    ):
        self.clean_train_set = clean_train_set
        self.clean_test_set = clean_test_set
        self.poison_train_set = poison_train_set
        self.poison_test_set = poison_test_set
        clean_train_loader = get_dataloader(
            dataset=clean_train_set,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=True,
        )
        clean_test_loader = get_dataloader(
            dataset=clean_test_set,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=True,
        )

        poison_test_loader = get_dataloader(
            dataset=poison_test_set,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=True,
        )
        poison_train_loader = get_dataloader(
            dataset=poison_train_set,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=collate_fn,
            shuffle=True,
            pin_memory=True,
        )
        self.model = model
        self.collate_fn = collate_fn
        self.fabric = L.Fabric(
            accelerator="gpu",
            devices=self.args.num_devices,
            strategy="ddp",
            precision="16-mixed",
        )
        self.fabric.launch()

        self.clean_train_loader = self.fabric.setup_dataloaders(clean_train_loader)
        self.clean_test_loader = self.fabric.setup_dataloaders(clean_test_loader)
        self.poison_train_loader = self.fabric.setup_dataloaders(poison_train_loader)
        self.poison_test_loader = self.fabric.setup_dataloaders(poison_test_loader)

    @abstractmethod
    def get_sanitized_lst(self):
        ...

    def train(self):
        indices = []
        for idx, is_clean in enumerate(self.is_clean_lst):
            if is_clean:
                indices.append(idx)
        self.sanitized_set = Subset(self.poison_train_set, indices)
        print(len(self.sanitized_set))
        self.sanitized_loader = get_dataloader(
            dataset=self.sanitized_set,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=self.collate_fn,
            shuffle=True,
            pin_memory=True,
        )
        self.sanitized_loader = self.fabric.setup_dataloaders(self.sanitized_loader)
        retrained_model, results = retraining(
            self.fabric,
            self.sanitized_loader,
            self.clean_test_loader,
            self.poison_test_loader,
            self.model,
            self.args,
        )
        print(results)
        return results


class PostTrainingBase(DefenseBase):
    def __init__(self, args) -> None:
        super().__init__(args)

    @abstractmethod
    def train(self):
        ...
