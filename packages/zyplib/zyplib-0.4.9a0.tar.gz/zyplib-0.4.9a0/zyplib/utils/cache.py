import functools
import os
from typing import Any, Callable, TypeVar

from diskcache import Cache, Timeout

from zyplib._config import config
from zyplib.utils import DottableDict
from zyplib.utils.print import print_warn

_configs = {'cache_dir': config.DISK_CACHE_DIR}


def update_cache_config(cache_dir: str = None):
    if cache_dir is not None:
        _configs['cache_dir'] = cache_dir


def cache_factory(cache_dir: str = None) -> Cache:
    cache_dir = os.path.join(_configs['cache_dir']) if cache_dir is None else cache_dir
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    return Cache(cache_dir)


def get_cache(key: str, default: Any = None):
    """获取缓存

    Parameters
    ----------
    - `key` : `str`
        - 缓存键
    - `default` : `Any`, optional
        - 默认值，当缓存不存在时返回

    Returns
    ----------
    - `Any`
        - 缓存值, 当缓存不存在或者过期时返回默认值
    """
    try:
        with cache_factory() as cache:
            return cache.get(key, default)
    except Timeout as t:
        print_warn(f'Cache[{key}] timeout: {t}')
        return default


def set_cache(key: str, value: Any, expire_seconds: int = None, tag: str = None):
    with cache_factory() as cache:
        flag = cache.set(key, value, expire=expire_seconds, tag=tag)
    if not flag:
        print_warn(f'Cache[{key}] set failed')
    return flag


def del_cache(key: str):
    with cache_factory() as cache:
        cache.delete(key)


def purge_all_cache():
    with cache_factory() as cache:
        cache.clear()


F = TypeVar('F', bound=Callable)


def make_func_memoize(
    func: F, cache: Cache, name=None, typed=False, expire=None, tag=None, ignore=()
) -> F:
    """接受一个函数对象，为其动态添加 diskcache 的 memoize 功能"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        memoized_func = cache.memoize(
            name=name, typed=typed, expire=expire, tag=tag, ignore=ignore
        )(func)
        return memoized_func(*args, **kwargs)

    return wrapper
