from abc import ABCMeta

from typing import Literal, Union

import torch
from torch import nn
from torch.nn import Module

XDim = Literal['1d', '2d', '3d', 1, 2, 3]
Conv = Union[nn.Conv1d, nn.Conv2d, nn.Conv3d]
BatchNorm = Union[nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d]
MaxPool = Union[nn.MaxPool1d, nn.MaxPool2d, nn.MaxPool3d]
AvgPool = Union[nn.AvgPool1d, nn.AvgPool2d, nn.AvgPool3d]
AdaptiveAvgPool = Union[nn.AdaptiveAvgPool1d, nn.AdaptiveAvgPool2d, nn.AdaptiveAvgPool3d]
AdaptiveMaxPool = Union[nn.AdaptiveMaxPool1d, nn.AdaptiveMaxPool2d, nn.AdaptiveMaxPool3d]
ConvTranspose = Union[nn.ConvTranspose1d, nn.ConvTranspose2d, nn.ConvTranspose3d]
Dropout = Union[nn.Dropout, nn.Dropout2d, nn.Dropout3d]


def conv(xdim: XDim = 1) -> Conv:
    if xdim == '1d':
        return nn.Conv1d
    elif xdim == '2d':
        return nn.Conv2d
    elif xdim == '3d':
        return nn.Conv3d
    elif xdim == 1:
        return nn.Conv1d
    elif xdim == 2:
        return nn.Conv2d
    elif xdim == 3:
        return nn.Conv3d
    else:
        raise ValueError(f'Invalid parameter xdim: {xdim}; 无法转换为对应的 Conv 类')


def batchnorm(xdim: XDim = 1) -> nn.Module:
    if xdim == '1d':
        return nn.BatchNorm1d
    elif xdim == '2d':
        return nn.BatchNorm2d
    elif xdim == '3d':
        return nn.BatchNorm3d
    elif xdim == 1:
        return nn.BatchNorm1d
    elif xdim == 2:
        return nn.BatchNorm2d
    elif xdim == 3:
        return nn.BatchNorm3d
    else:
        raise ValueError(f'Invalid parameter xdim: {xdim}; 无法转换为对应的 BatchNorm 类')


def maxpool(xdim: XDim = 1) -> MaxPool:
    if xdim == '1d':
        return nn.MaxPool1d
    elif xdim == '2d':
        return nn.MaxPool2d
    elif xdim == '3d':
        return nn.MaxPool3d
    elif xdim == 1:
        return nn.MaxPool1d
    elif xdim == 2:
        return nn.MaxPool2d
    elif xdim == 3:
        return nn.MaxPool3d
    else:
        raise ValueError(f'Invalid parameter xdim: {xdim}; 无法转换为对应的 MaxPool 类')


def avgpool(xdim: XDim = 1) -> AvgPool:
    if xdim == '1d':
        return nn.AvgPool1d
    elif xdim == '2d':
        return nn.AvgPool2d
    elif xdim == '3d':
        return nn.AvgPool3d
    elif xdim == 1:
        return nn.AvgPool1d
    elif xdim == 2:
        return nn.AvgPool2d
    elif xdim == 3:
        return nn.AvgPool3d
    else:
        raise ValueError(f'Invalid parameter xdim: {xdim}; 无法转换为对应的 AvgPool 类')


def adaptiveavgpool(xdim: XDim = 1) -> AdaptiveAvgPool:
    if xdim == '1d':
        return nn.AdaptiveAvgPool1d
    elif xdim == '2d':
        return nn.AdaptiveAvgPool2d
    elif xdim == '3d':
        return nn.AdaptiveAvgPool3d
    elif xdim == 1:
        return nn.AdaptiveAvgPool1d
    elif xdim == 2:
        return nn.AdaptiveAvgPool2d
    elif xdim == 3:
        return nn.AdaptiveAvgPool3d
    else:
        raise ValueError(
            f'Invalid parameter xdim: {xdim}; 无法转换为对应的 AdaptiveAvgPool 类'
        )


def adaptivemaxpool(xdim: XDim = 1) -> AdaptiveMaxPool:
    if xdim == '1d':
        return nn.AdaptiveMaxPool1d
    elif xdim == '2d':
        return nn.AdaptiveMaxPool2d
    elif xdim == '3d':
        return nn.AdaptiveMaxPool3d
    elif xdim == 1:
        return nn.AdaptiveMaxPool1d
    elif xdim == 2:
        return nn.AdaptiveMaxPool2d
    elif xdim == 3:
        return nn.AdaptiveMaxPool3d
    else:
        raise ValueError(
            f'Invalid parameter xdim: {xdim}; 无法转换为对应的 AdaptiveMaxPool 类'
        )


def convtranspose(xdim: XDim = 1) -> ConvTranspose:
    if xdim == '1d':
        return nn.ConvTranspose1d
    elif xdim == '2d':
        return nn.ConvTranspose2d
    elif xdim == '3d':
        return nn.ConvTranspose3d
    elif xdim == 1:
        return nn.ConvTranspose1d
    elif xdim == 2:
        return nn.ConvTranspose2d
    elif xdim == 3:
        return nn.ConvTranspose3d
    else:
        raise ValueError(
            f'Invalid parameter xdim: {xdim}; 无法转换为对应的 ConvTranspose 类'
        )


def dropout(xdim: XDim = 1) -> Dropout:
    if xdim == '1d':
        return nn.Dropout
    elif xdim == '2d':
        return nn.Dropout2d
    elif xdim == '3d':
        return nn.Dropout3d
    elif xdim == 1:
        return nn.Dropout
    elif xdim == 2:
        return nn.Dropout2d
    elif xdim == 3:
        return nn.Dropout3d
    else:
        raise ValueError(f'Invalid parameter xdim: {xdim}; 无法转换为对应的 Dropout 类')


class BaseModule(Module):
    __metaclass__ = ABCMeta

    def __hash__(self) -> int:
        return hash(str(self))

    def init_weights(self, weight_init_func=None):
        if weight_init_func is None:
            self.apply(self.default_init_weights)
        else:
            self.apply(weight_init_func)

    def default_init_weights(self, m):
        if isinstance(m, (nn.Conv1d, nn.Conv2d, nn.Conv3d)):
            nn.init.kaiming_uniform_(m.weight.data, nonlinearity='leaky_relu')
            if m.bias is not None:
                nn.init.constant_(m.bias.data, 0)
        elif isinstance(m, (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d)):
            nn.init.constant_(m.weight.data, 1)
            if m.bias is not None:
                nn.init.constant_(m.bias.data, 0)
        elif isinstance(m, nn.Linear):
            nn.init.kaiming_uniform_(m.weight.data)
            if m.bias is not None:
                nn.init.constant_(m.bias.data, 0)
