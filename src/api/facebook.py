from src.api import Api


class Facebook(Api):

    def register(self, webhook):
        raise NotImplementedError

    def send_message(self, chat_id, text):
        raise NotImplementedError

    def receive_message(self):
        raise NotImplementedError
