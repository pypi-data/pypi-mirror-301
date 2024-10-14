import torch
from torch.utils.data import Dataset, DataLoader, random_split


def train_val_split(
    data_set: Dataset, val_proportion: float, n_batch: int
) -> (DataLoader, DataLoader):
    """Split DataSet into TrainDataLoader and ValDataLoader"""
    n_data = len(data_set)
    n_val = int(n_data * val_proportion)
    n_train = n_data - n_val
    train_set, val_set = random_split(data_set, [n_train, n_val])
    train_data_loader = DataLoader(
        train_set, batch_size=n_batch, drop_last=True, num_workers=1, pin_memory=True
    )
    val_data_loader = DataLoader(
        val_set, batch_size=n_batch, drop_last=True, num_workers=1, pin_memory=True
    )
    return train_data_loader, val_data_loader
