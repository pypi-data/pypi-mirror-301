from .client import QCClient
from .config import QCConfig
from .job import QCJob
from typing import Union

import sys
import logging

def _timestamp_formatter(with_lineno: bool = False) -> logging.Formatter:
    return logging.Formatter(
        fmt='[%(asctime)s PID %(process)d] %(levelname)s %(message)s'
        if not with_lineno else '[%(asctime)s PID %(process)d] %(levelname)s %(message)s \t(%(pathname)s:%(lineno)d)',
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def setup_default_logging(stdout: bool = True,
                          *,
                          file_path=None,
                          file_mode='a',
                          level=logging.INFO,
                          formatter: Union[str, logging.Formatter] = 'time'):
    if formatter == 'time':
        formatter = _timestamp_formatter()
    elif formatter == 'lineno':
        formatter = _timestamp_formatter(with_lineno=True)
    elif not isinstance(formatter, logging.Formatter):
        raise ValueError(f'invalid formatter {formatter}')

    logger = logging.getLogger()
    logger.setLevel(level)

    # clear old handlers
    logger.handlers = []

    if stdout:
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    if file_path != None:
        file_handler = logging.FileHandler(file_path, mode=file_mode)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
