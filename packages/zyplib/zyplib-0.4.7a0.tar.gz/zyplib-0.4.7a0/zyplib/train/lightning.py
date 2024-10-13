from typing import Dict, Optional, Union

import lightning as L
import torch
from torch import nn
from torch.optim.lr_scheduler import _LRScheduler
from torchmetrics import Metric, MetricCollection


class BasicLightningTrainer(L.LightningModule):
    def __init__(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        fn_loss: nn.Module = None,
        metrics: Optional[Union[MetricCollection, Dict[str, Metric]]] = None,
        lr_scheduler: Optional[_LRScheduler] = None,
        lr_sched_freq: int = 1,
        lr_sched_interval: str = 'epoch',
    ):
        """一个基础常用的 LightningModule Trainer

        Parameters
        ----------
        - `model` : `nn.Module`
            - 模型
        - `optimizer` : `torch.optim.Optimizer`
            - 优化器
        - `fn_loss` : `nn.Module`, optional
            - 损失函数
        - `metrics` : `MetricCollection | Dict[str, Metric]`, optional
            - 评估指标
            - 使用 `torchmetrics.MetricCollection` 或 `dict` 类型
        - `lr_scheduler` : `torch.optim.lr_scheduler._LRScheduler`, optional
            - 学习率调度器
        - `lr_sched_freq` : `int`, optional
            - 学习率调度器更新频率
        - `lr_sched_interval` : `str`, optional
            - 学习率调度器更新间隔
        """
        super().__init__()
        self.model = model
        self.optimizer = optimizer
        self.fn_loss = fn_loss or nn.CrossEntropyLoss()
        if metrics is None:
            self.metrics = MetricCollection({})
        elif isinstance(metrics, dict):
            self.metrics = MetricCollection(metrics)
        else:
            self.metrics = metrics
        self.lr_scheduler = lr_scheduler
        self.lr_sched_freq = lr_sched_freq
        self.lr_sched_interval = lr_sched_interval

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = self.fn_loss(y_hat, y)
        self.log('train_loss', loss, prog_bar=True, on_step=True, on_epoch=True)

        # Update and log metrics
        for metric_name, metric in self.metrics.items():
            metric_value = metric(y_hat, y)
            self.log(
                f'train_{metric_name}',
                metric_value,
                prog_bar=True,
                on_step=True,
                on_epoch=True,
            )

        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = self.fn_loss(y_hat, y)
        self.log('val_loss', loss, prog_bar=True, on_epoch=True)

        # Update and log metrics
        for metric_name, metric in self.metrics.items():
            metric_value = metric(y_hat, y)
            self.log(f'val_{metric_name}', metric_value, prog_bar=True, on_epoch=True)

        return loss

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = self.fn_loss(y_hat, y)
        self.log('test_loss', loss, prog_bar=True, on_epoch=True)

        # Update and log metrics
        for metric_name, metric in self.metrics.items():
            metric_value = metric(y_hat, y)
            self.log(f'test_{metric_name}', metric_value, prog_bar=True, on_epoch=True)

        return loss

    def configure_optimizers(self):
        if self.lr_scheduler is None:
            return self.optimizer
        return {
            'optimizer': self.optimizer,
            'lr_scheduler': {
                'scheduler': self.lr_scheduler,
                'interval': self.lr_sched_interval,
                'frequency': self.lr_sched_freq,
            },
        }

    # def on_train_epoch_end(self):
    #     for metric_name, metric in self.metrics.items():
    #         self.log(f'Train/{metric_name}', metric.compute())
    #         metric.reset()

    # def on_validation_epoch_end(self):
    #     for metric_name, metric in self.metrics.items():
    #         self.log(f'Val/{metric_name}', metric.compute())
    #         metric.reset()

    # def on_test_epoch_end(self):
    #     for metric_name, metric in self.metrics.items():
    #         self.log(f'Test/{metric_name}', metric.compute())
    #         metric.reset()
