from typing import Sequence, Union

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from torch.utils.data import random_split as torch_random_split

from zyplib.utils.ensure import ensure_tensor


class BasicXyDataset(Dataset):
    def __init__(
        self,
        data: Union[np.ndarray, torch.Tensor],
        labels: Union[np.ndarray, torch.Tensor],
    ):
        self.data = ensure_tensor(data)
        self.labels = ensure_tensor(labels)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


def make_dataloader_from_xy(
    xy_train: tuple[np.ndarray, np.ndarray],
    xy_test: tuple[np.ndarray, np.ndarray] = None,
    split_val_from_train: Sequence[Union[int, float]] = None,
    batch_size: int = 64,
    shuffle: bool = True,
    num_workers: int = 0,
    pin_memory: bool = False,
    **kwargs,
):
    """从训练和测试数据创建 DataLoader(s)。
    
    参数
    ----------
    - `xy_train` : `tuple[np.ndarray, np.ndarray]`
        - 包含训练数据和标签的元组。
    - `xy_test` : `tuple[np.ndarray, np.ndarray]`, 可选
        - 包含测试数据和标签的元组，默认为 None。
    - `split_val_from_train` : `tuple[float, float] | tuple[int, int]`, 可选
        - 指定如何将训练数据拆分为训练集和验证集，默认为 None。
        - 如果为 None，则不进行拆分。
    - `batch_size` : `int`, 可选
        - 每个批次的样本数量，默认为 64。
    - `shuffle` : `bool`, 可选
        - 是否在每个 epoch 时打乱数据，默认为 True。
    - `num_workers` : `int`, 可选
        - 用于数据加载的子进程数量，默认为 0。
    - `pin_memory` : `bool`, 可选
        - 如果为 True，数据加载器将把张量复制到 CUDA 固定内存中，默认为 False。
    - `**kwargs` : `dict`, 可选
        - DataLoader 的其他参数，默认为 None。
    
    返回
    ----------
    - `tuple[DataLoader]`
        - 训练、验证和测试数据集的 DataLoader 元组。
    """
    train_dataset = BasicXyDataset(*xy_train)

    if xy_test is not None:
        test_dataset = BasicXyDataset(*xy_test)
    else:
        test_dataset = None

    # 划分验证集
    if split_val_from_train:
        train_dataset, val_dataset = torch_random_split(
            train_dataset, split_val_from_train
        )
    else:
        val_dataset = None

    def make_dataloader(dataset: Dataset):
        if dataset is None:
            return None
        return DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers,
            pin_memory=pin_memory,
            **kwargs,
        )

    loaders = map(make_dataloader, [train_dataset, val_dataset, test_dataset])
    loaders = filter(lambda x: x is not None, loaders)
    return tuple(loaders)
