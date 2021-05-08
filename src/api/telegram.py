import requests
import flask
from src.api import Api
from flask import request
from src.intents.pizza import Pizza
import json
import time
from threading import Thread, Lock


class Telegram(Api):
    """
    Telegram api(no libs)
    """
    def __init__(self, token: str, api: str, webhook: str):
        super().__init__()
        self.token = token                              # Bot token
        self.api = api                                  # Telegram api url
        self.webhook = webhook                          # Webhook
        self.telegram_url = f"{self.api}{self.token}"   # api + token
        self.clients = {}                               # Simple clients dict

    def register(self, app: flask.Flask):
        """
        Register url rule for this api webhook
        :return:
        """
        try:
            self.set_webhook()
        except Exception as e:
            self.logger.warning(f"Error due to setting telegram webhook -> {e}")
        else:
            app.add_url_rule('/telegram', 'telegram', self.receive_message, methods=["POST"])

    def send_message(self, chat_id, text):
        """
        Send message (text only)
        :param chat_id: user chat id
        :param text: user text
        :return:
        """
        method = "sendMessage"
        url = f"{self.telegram_url}/{method}"
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)

    def set_webhook(self):
        """
        Try set webhook
        :return:
        """
        method = "setWebhook"
        url = f"{self.telegram_url}/{method}"
        resp = requests.post(url, data={"url": self.webhook})
        resp = json.loads(resp.text)
        if resp['ok']:
            self.logger.info('Webhook was set!')
        else:
            raise Exception(f"Cannot set webhook -> {resp}")

    def message_handle(self, chat_id, text):
        """
        Handling message from user
        User is new if message = "/start"
        Otherwise create or continue user intent (only pizza intent available)
        :param chat_id: user chat id
        :param text: user text
        :return:
        """
        if text == '/start':
            self.send_message(chat_id, text="Привет! Напишите любой текст, чтобы начать заказывать пиццу. Если захотите прервать диалог напишите \"Выход\"")
        else:
            # Here should be intent recognition module(ai, simple rules) but in this case only pizza intent is available
            if chat_id not in self.clients:
                self.clients[chat_id] = Pizza(self)
            client_intent = self.clients.get(chat_id)
            client_intent.next(chat_id=chat_id, text=text)

    def receive_message(self):
        """
        Webhook callback
        Every message handling by this method
        Message will be skipped if it is not text type message
        :return:
        """
        self.logger.info(f"Get updates: {request.json}")
        try:
            chat_id = request.json["message"]["chat"]["id"]
        except KeyError as e:
            self.logger.warning(f"Message skipped due to chat_id does not present")
        else:
            try:
                text = request.json["message"]["text"]
            except KeyError as e:
                self.send_message(chat_id, text="Я понимаю только текстовые сообщения!")
            else:
                self.logger.info(f"Get message: chat_id: {chat_id} text: {text}")
                self.message_handle(chat_id, text)

        return {'ok': True}
