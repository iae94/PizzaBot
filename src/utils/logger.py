import logging, sys
from src.utils import Singleton


class Logger(metaclass=Singleton):

    def __init__(self):

        # Logger
        self.logger_name = 'Pizza Bot'

        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        formatter = logging.Formatter('[%(asctime)s] - %(name)-15s - %(module)-10s - [%(levelname)-8s] - %(threadName)-15s - %(message)s')

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        self.logger = logger

    def get(self):
        return self.logger