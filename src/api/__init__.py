from abc import ABC, abstractmethod
from src.utils.logger import Logger


class Api(ABC):
    """
    Abstract class for api
    """
    def __init__(self):
        self.logger = Logger().get()

    @abstractmethod
    def send_message(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def register(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def receive_message(self, *args, **kwargs):
        raise NotImplementedError
