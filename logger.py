"""Rotating file logger shared by all modules."""
import logging
from logging.handlers import RotatingFileHandler

from . import config


def get_logger(name: str = "studysprint") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    try:
        config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(config.LOG_FILE, maxBytes=200_000, backupCount=2)
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(handler)
    except OSError:  # read-only file system etc. -> fall back silently
        logger.addHandler(logging.NullHandler())
    logger.propagate = False
    return logger
