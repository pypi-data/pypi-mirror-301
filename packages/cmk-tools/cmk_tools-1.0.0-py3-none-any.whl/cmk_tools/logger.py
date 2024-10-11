import logging
import os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler


def setup_time_rotation_logger(name, level):
    log_file_dir = os.path.join(Path.home(), 'cmkredisutils', 'logs')
    if not os.path.isdir(log_file_dir):
        os.makedirs(log_file_dir, exist_ok=True)
    log_file_path = os.path.join(log_file_dir, f'{name}.log')
    print('log files will be saved at:', log_file_path)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    handler.setLevel(level)
    logger.addHandler(handler)
    return logger

