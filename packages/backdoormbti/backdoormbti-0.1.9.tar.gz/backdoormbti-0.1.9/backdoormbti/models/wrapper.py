import logging
import time

import lightning as L
import torch
import torch.nn.functional as F
from torchmetrics import Accuracy

from backdoormbti.utils.data import get_dataloader
from backdoormbti.utils.optim import get_optimizer, get_lr_scheduler


class BaseModelWrapper(L.LightningModule):
    def __init__(self, model, args):
        super().__init__()
        self.save_hyperparameters(ignore=["model"])
        self.model = model
        self.args = args
        self.acc = Accuracy(task="multiclass", num_classes=self.args.num_classes)

        # batch size finder
        self.collate_fn = self.args.collate_fn
        self.dataset = self.args.train_set
        self.batch_size = 2

    def train_dataloader(self):
        self.args.batch_size = self.batch_size
        logging.info(
            "update args.batch_size to: {batch_size}".format(batch_size=self.batch_size)
        )
        return get_dataloader(
            dataset=self.dataset,
            batch_size=self.batch_size,
            num_workers=self.args.num_workers,
            collate_fn=self.collate_fn,
            shuffle=True,
        )

    def on_train_epoch_start(self) -> None:
        self.time = time.time()
        return super().on_train_epoch_start()

    def training_step(self, batch, batch_idx):
        pass

    def on_train_epoch_end(self) -> None:
        train_time = time.time() - self.time
        self.log("training_time", train_time)

        return super().on_train_epoch_end()

    def test_step(self, batch, batch_idx, dataloader_idx=0):
        pass

    def configure_optimizers(self):
        optimizer = get_optimizer(
            self.args.client_optimizer,
            self.parameters(),
            lr=self.args.lr,
            weight_decay=self.args.weight_decay,
        )
        scheduler = get_lr_scheduler(self.args.lr_scheduler, optimizer, self.args)
        return [optimizer], [scheduler]
        # if self.args.lr_scheduler != "None":
        #     scheduler = get_lr_scheduler(self.args.lr_scheduler, optimizer, self.args)
        #     return [optimizer], [scheduler]
        # else:
        #     return optimizer

class ImageModelWrapper(BaseModelWrapper):
    def __init__(self, model, args):
        super().__init__(model, args)

    def training_step(self, batch, batch_idx):
        x, y, is_poison, y_original = batch
        z = self.model(x)
        loss = F.cross_entropy(z, y)
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
        return loss

    def test_step(self, batch, batch_idx, dataloader_idx=0):
        x, y, is_poison, y_original = batch
        z = self.model(x)
        loss = F.cross_entropy(z, y)

        clean_acc = self.acc(z, y_original)
        if dataloader_idx == 0:
            self.log("test_clean_acc", clean_acc)
            return loss, clean_acc
        if dataloader_idx == 1:
            ra = clean_acc
            asr = self.acc(z, y)
            self.log("test_ra", ra)
            self.log("test_asr", asr)
            return loss, ra, asr

class TextModelWrapper(BaseModelWrapper):
    def __init__(self, model, args):
        super().__init__(model, args)

    def training_step(self, batch, batch_idx):
        text, labels, is_poison, pre_label = batch
        inputs = self.args.tokenizer(
            text, padding=True, truncation=True, return_tensors="pt"
        )
        inputs["labels"] = labels
        inputs = inputs.to("cuda")
        ret = self.model(**inputs)
        loss = ret.loss
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
        return loss

    def test_step(self, batch, batch_idx, dataloader_idx=0):
        text, label, is_poison, pre_label = batch
        inputs = self.args.tokenizer(
            text, padding=True, truncation=True, return_tensors="pt"
        )
        inputs.to("cuda")
        ret = self.model(**inputs)
        logits = ret[0]

        clean_acc = self.acc(logits, pre_label)
        if dataloader_idx == 0:
            self.log("test_clean_acc", clean_acc, batch_size=len(batch))
            return clean_acc
        if dataloader_idx == 1:
            ra = clean_acc
            asr = self.acc(logits, label)
            self.log("test_ra", ra, batch_size=len(batch))
            self.log("test_asr", asr, batch_size=len(batch))
            return ra, asr


class AudioModelWrapper(BaseModelWrapper):
    def __init__(self, model, args):
        super().__init__(model, args)

    def label_to_index(self, word):
        # Return the position of the word in labels
        return torch.tensor(self.args.classes.index(word))

    def training_step(self, batch, batch_idx):
        waveform, target, is_poison, label_original = batch
        if self.args.model in ["lstm", "xvector"]:
            waveform = self.args.pre_trans(waveform)
        preds = self.model(waveform)
        target = target.cuda()
        preds = preds.squeeze(1)
        loss = F.cross_entropy(preds, target)
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
        return loss

    def test_step(self, batch, batch_idx, dataloader_idx=0):
        waveform, target, is_poison, pre_target = batch
        if self.args.model in ["lstm", "xvector"]:
            waveform = self.args.pre_trans(waveform)
        preds = self.model(waveform)
        target = target.cuda()

        loss = F.cross_entropy(preds.squeeze(), target)

        preds = preds.squeeze().argmax(1)
        clean_acc = self.acc(preds, pre_target)
        if dataloader_idx == 0:
            self.log("test_clean_acc", clean_acc)
            return loss, clean_acc
        if dataloader_idx == 1:
            ra = clean_acc
            asr = self.acc(preds, target)
            self.log("test_ra", ra)
            self.log("test_asr", asr)
            return loss, ra, asr


class VideoModelWrapper(BaseModelWrapper):
    def __init__(self, model, args):
        super().__init__(model, args)

    def training_step(self, batch, batch_idx):
        video, label, is_poison, pre_label = batch
        preds = self.model(video)
        label = label.cuda()
        loss = F.cross_entropy(preds, label)
        self.log("train_loss", loss)
        return loss

    def test_step(self, batch, batch_idx, dataloader_idx=0):
        video, label, is_poison, pre_label = batch
        preds = self.model(video)
        loss = F.cross_entropy(preds, label)
        preds = preds.argmax(1)

        clean_acc = self.acc(preds, pre_label)
        if dataloader_idx == 0:
            self.log("test_clean_acc", clean_acc)
            return loss, clean_acc
        if dataloader_idx == 1:
            ra = clean_acc
            asr = self.acc(preds, label)
            self.log("test_ra", ra)
            self.log("test_asr", asr)
            return loss, ra, asr
