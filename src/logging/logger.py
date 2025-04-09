import logging
import sys

def project_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    _DEFAULT_FORMAT = '%(asctime)s|%(name)s|%(levelname)-.1s|%(message)s'
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_DEFAULT_FORMAT))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


