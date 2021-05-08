from src.api import Api


class Vk(Api):

    def register(self, webhook):
        raise NotImplementedError

    def send_message(self, chat_id, text):
        raise NotImplementedError

    def receive_message(self):
        raise NotImplementedError
