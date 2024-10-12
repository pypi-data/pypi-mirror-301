"""
本模块主要提供了一些数据集导入的 pipeline 相关的函数，是对脑电信号数据导入、预处理流程的高级封装

所有函数均满足:

- 输入: 一些参数，以及一些回调函数
- 输出: 返回数据集 (X, y)

"""
from functools import reduce
from typing import Callable, Union

import numpy as np

__all__ = ['basic_pipeline']



def basic_pipeline(
    files: list[str],
    fn_read: Callable[[str], np.ndarray],
    fn_segment: Callable[[np.ndarray], np.ndarray],
    label: Union[int, Callable[[str], int]],
    fn_before_segment: Callable[[np.ndarray], np.ndarray] = None,
    fn_after_segment: Callable[[np.ndarray], np.ndarray] = None,
):
    """从文件中读取数据，并自动切片、制作用于训练的数据集

    本 Pipeline 适用于:
    - 从文件中读取完整的脑电
    - 需要对完整脑电进行切分
    - 无特殊标签，只需根据文件进行标记即可
    - 输出: 数据集 (X, y)
        - X: 数据，shape = (N, C, T)
        - y: 标签，shape = (N,)

    Pipeline 流程:
    ----------

    1. 从文件中读取完整的数据 X
    2. 对数据 X 进行预处理
    3. 对数据 X 进行切片
    4. 对数据 X 进行后处理
    5. 制作标签 y
    6. 返回数据集 (X, y)

    Parameters
    ----------
    - `files` : `list[str]`
        - 文件路径列表
    - `fn_read` : `(file_path: str) -> np.ndarray`
        - 文件读取函数
    - `fn_segment` : `(signal: np.ndarray) -> np.ndarray`
        - 数据切片函数
        - 输入一个 `[C, T]` 的信号
        - 输出一个 `[N, C, T]` 的信号
    - `label` : `int | (file_path: str) -> int`
        - 标签，如果为 int，则所有数据标签相同；如果为函数，则根据文件名生成标签
    - `fn_before_segment` : `(signal: [C, T]) -> [C, T]`, optional
        - 数据切片前的处理函数
    - `fn_after_segment` : `(signal: [N, C, T]) -> [N, C, T]`, optional
        - 数据切片后的处理函数

    Returns
    ----------
    - `X` : `np.ndarray`, shape = (N, C, T)
        - 数据
    - `y` : `np.ndarray`, shape = (N,)
        - 标签
    """
    if not files:
        raise ValueError('The files list is empty. Please provide at least one file.')

    fn_before_segment = fn_before_segment or (lambda x: x)
    fn_after_segment = fn_after_segment or (lambda x: x)
    label = label if callable(label) else (lambda _: label)

    # 处理单个文件
    def load_single_file(fpath: str):
        signal = fn_read(fpath)  # 读取数据
        signal = fn_before_segment(signal)  # 数据预处理
        segments = fn_segment(signal)  # 数据切片
        segments = fn_after_segment(segments)
        N = len(segments)
        label_ = label(fpath)  # 制作标签
        return segments, [label_] * N

    # 批量处理所有文件
    results = map(load_single_file, files)

    # 合并数据
    def merge_data(Xy: tuple[list[np.ndarray], list[int]], pair: tuple[np.ndarray, int]):
        Xy[0].append(pair[0])
        Xy[1].extend(pair[1])
        return Xy

    Xy = reduce(merge_data, results, ([], []))

    X = np.concatenate(Xy[0], axis=0)
    y = np.array(Xy[1], dtype=int)
    return X, y
