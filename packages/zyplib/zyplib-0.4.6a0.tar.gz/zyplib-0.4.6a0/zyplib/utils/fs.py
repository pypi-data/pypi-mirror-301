"""
文件系统相关工具
"""

import json
import os
import shutil
from pathlib import Path
from typing import Literal, Union

import yaml

from .print import debug

FilePath = Union[Path, str]


def ensure_dir(dir: str, if_not_empty: Literal['keep', 'clean', 'error'] = 'keep'):
    """检查用于保存日志、Checkpoint 等的目录如果 dir 不存在，则创建

    Parameters
    ----------
    - `dir` : `str`
        - 目录
    - `if_not_empty` : `Literal['keep', 'clean', 'error']`, optional
        - 如果目录不为空，则执行的操作
        - `"keep"` | `"clean"` | `"error"`
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
    elif any(os.scandir(dir)):
        if if_not_empty is None or if_not_empty == 'keep':
            debug(f'Exists: {dir}!')
        elif if_not_empty == 'clean':
            debug(f'Clean up: {dir}!')
            shutil.rmtree(dir)
            os.makedirs(dir)
        elif if_not_empty == 'error':
            raise Exception(f'目录 {dir} 不为空!')
        else:
            raise ValueError(f'check_dir 参数错误: if_not_empty = {if_not_empty}')


def file_reader(file_path: FilePath, encoding: str = 'utf-8', binary: bool = False):
    mode = 'rb' if binary else 'r'
    return open(file_path, mode, encoding=None if binary else encoding)


def read_file(
    file_path: FilePath,
    encoding: str = 'utf-8',
    binary: bool = False,
    readlines: bool = False,
) -> str | list[str]:
    with file_reader(file_path, encoding, binary) as f:
        if readlines:
            return f.readlines()
        return f.read()


def file_writer(file_path: FilePath, encoding: str = 'utf-8', binary: bool = False):
    mode = 'wb' if binary else 'w'
    return open(file_path, mode, encoding=None if binary else encoding)


def write_file(
    file_path: FilePath,
    content: str | bytes,
    encoding: str = 'utf-8',
    binary: bool = False,
):
    with file_writer(file_path, encoding, binary) as f:
        f.write(content)


def read_json(file_path: FilePath, encoding: str = 'utf-8'):
    with open(file_path, 'r', encoding=encoding) as f:
        return json.load(f)


def write_json(file_path: FilePath, data: dict, encoding: str = 'utf-8'):
    with open(file_path, 'w', encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_yaml(file_path: FilePath, throw_error: bool = True):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        if throw_error:
            raise e
        return {}


def write_yaml(file_path: FilePath, data: dict):
    def str_presenter(dumper, data):
        if len(data.splitlines()) > 1:  # check for multiline string
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    yaml.add_representer(str, str_presenter)

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
