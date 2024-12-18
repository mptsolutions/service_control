"""
    This module provides simplified logging options.
    Logging parameters can be set in config.py
    It is used by importing this module in the main module.
"""

import logging
from sys import stdout
from config import LOG_LEVEL, LOG_FILE_PATH, LOG_FILE_MODE

log_format = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s", "%Y-%m-%d %H:%M:%S")

log_stdout = logging.StreamHandler(stream=stdout)
log_stdout.setFormatter(log_format)
logging.getLogger().setLevel(LOG_LEVEL)
logging.getLogger().addHandler(log_stdout)

if LOG_FILE_PATH is not None:
    log_fileout = logging.FileHandler(filename=LOG_FILE_PATH, mode=LOG_FILE_MODE)
    log_fileout.setFormatter(log_format)
    logging.getLogger().addHandler(log_fileout)

logging.debug("Initialized log handler")