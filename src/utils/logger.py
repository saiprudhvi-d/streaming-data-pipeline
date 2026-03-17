import logging, sys

def get_logger(name):
    logger = logging.getLogger(name)
    if logger.handlers: return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)-5s - %(message)s")
    ch = logging.StreamHandler(sys.stdout); ch.setFormatter(fmt); logger.addHandler(ch)
    return logger
