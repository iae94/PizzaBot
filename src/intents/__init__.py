from abc import ABC, abstractmethod
from src.utils.logger import Logger


class Intent(ABC):
    def __init__(self):
        self.logger = Logger().get()