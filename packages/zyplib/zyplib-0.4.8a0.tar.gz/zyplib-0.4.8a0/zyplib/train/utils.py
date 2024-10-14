import os
import random
from functools import lru_cache
from typing import Union

import numpy as np
import torch
from torch import nn


def seed_everything(seed: int):
    os.environ['PL_GLOBAL_SEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


@lru_cache
def cuda_available():
    return torch.cuda.is_available()


def use_device(x: Union[torch.Tensor, nn.Module], DEVICE='cuda', hint=False):
    if cuda_available():
        if hint:
            print(f'{x.__class__.__name__} To Cuda!')
        return x.to(DEVICE)
    else:
        return x
