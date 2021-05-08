from abc import ABC, abstractmethod
from src.utils.logger import Logger


class Api(ABC):
    def __init__(self, app):
        self.app = app
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
