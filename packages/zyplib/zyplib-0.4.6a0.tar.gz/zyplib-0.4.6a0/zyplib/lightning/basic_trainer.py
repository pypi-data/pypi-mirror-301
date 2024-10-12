import lightning as L
import torch
from torch import nn


class BasicClassifier(L.LightningModule):
    def __init__(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        loss_fn: nn.Module = None,
        metrics: dict = None,
    ):
        super().__init__()
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn or nn.CrossEntropyLoss()
        self.metrics = metrics or {}

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = self.loss_fn(y_hat, y)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = self.loss_fn(y_hat, y)
        self.log('val_loss', loss)
        return loss

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = self.loss_fn(y_hat, y)
        self.log('test_loss', loss)
        return loss

    def configure_optimizers(self):
        return self.optimizer

    def on_train_epoch_end(self):
        for metric_name, metric in self.metrics.items():
            self.log(f'Train/{metric_name}', metric.compute())
            metric.reset()

    def on_validation_epoch_end(self):
        for metric_name, metric in self.metrics.items():
            self.log(f'Val/{metric_name}', metric.compute())
            metric.reset()

    def on_test_epoch_end(self):
        for metric_name, metric in self.metrics.items():
            self.log(f'Test/{metric_name}', metric.compute())
            metric.reset()
