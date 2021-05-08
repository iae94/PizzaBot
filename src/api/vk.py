from src.api import Api


class Vk(Api):
    """
    Vk not implemented
    """
    def register(self):
        raise NotImplementedError

    def send_message(self, chat_id, text):
        raise NotImplementedError

    def receive_message(self):
        raise NotImplementedError
