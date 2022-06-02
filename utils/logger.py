import logging
import os

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

log_path = os.path.join(os.getcwd(), "logs")

def setup_logger(name, log_file, level=logging.DEBUG):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(os.path.join(log_path, log_file))
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger