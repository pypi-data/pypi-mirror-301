import os

from zyplib._config import config


def _get_cache_dir():
    return os.path.join(config.DISK_CACHE_DIR, 'cache')

#TODO 使用 diskcache 实现缓存
