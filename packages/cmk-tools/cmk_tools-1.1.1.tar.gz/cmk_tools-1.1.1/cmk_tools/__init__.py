# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>


__version__ = '1.1.1'


import logging

from .logger import setup_time_rotation_logger
from .redis_semaphore import (
    RedisSemaphore,
    run_with_semaphore,
    run_with_semaphore_decorator,
)

logger = setup_time_rotation_logger(
    "redis_semaphore",
    logging.DEBUG,
    format_json=True,
)


__all__ = [
    "RedisSemaphore",
    "run_with_semaphore",
    "run_with_semaphore_decorator",
]
