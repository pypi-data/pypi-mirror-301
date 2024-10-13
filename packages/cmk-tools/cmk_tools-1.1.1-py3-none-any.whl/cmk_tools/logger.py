# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

import logging
import os
import json
from typing import Callable
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger


def json_translate_obj(obj):
    # for example, serialize a custom object
    # if isinstance(obj, MyClass):
    #     return {"special": obj.special}
    return {'obj': str(obj)}


def setup_time_rotation_logger(
    name, 
    level, 
    log_file_dir=None, 
    format_json=False, 
    json_translator=json_translate_obj
):
    if not log_file_dir:
        log_file_dir = os.path.join(Path.home(), "cmk-tools", "logs")

    if not os.path.isdir(log_file_dir):
        os.makedirs(log_file_dir, exist_ok=True)
    
    log_file_path = os.path.join(log_file_dir, f"{name}.log")
    print("log files will be saved at:", log_file_path)

    logger = logging.getLogger(f'cmk-tools.{name}')
    logger.setLevel(logging.DEBUG)

    handler = TimedRotatingFileHandler(
        log_file_path, when="midnight", interval=1, backupCount=7
    )

    if format_json:
        formatter = jsonlogger.JsonFormatter(
            json_encoder=json.JSONEncoder,
            json_default=json_translator,
        )
    else:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    return logger
