import requests
import flask
from src.api import Api
from flask import request
from src.intents.pizza import Pizza
import json
import time
from threading import Thread, Lock


class Telegram(Api):
    def __init__(self, token: str, api: str, webhook: str, app: flask.Flask):
        super().__init__(app)
        self.token = token
        self.api = api
        self.webhook = webhook
        self.telegram_url = f"{self.api}{self.token}"
        self.clients = {}

    def register(self):
        try:
            self.set_webhook()
        except Exception as e:
            self.logger.warning(f"Error due to setting telegram webhook -> {e}")
        else:
            self.app.add_url_rule('/telegram', 'telegram', self.receive_message, methods=["POST"])

    def send_message(self, chat_id, text):
        method = "sendMessage"
        url = f"{self.telegram_url}/{method}"
        data = {"chat_id": chat_id, "text": text}
        resp = requests.post(url, data=data)
        self.logger.info(json.loads(resp.text))

    def set_webhook(self):
        method = "setWebhook"
        url = f"{self.telegram_url}/{method}"
        data = {"url": self.webhook}
        resp = requests.post(url, data=data)
        resp = json.loads(resp.text)
        if resp['ok']:
            self.logger.info('Webhook was set!')
        else:
            raise Exception(f"Cannot set webhook -> {resp}")

    def get_updates(self):

        while True:

            method = "getUpdates"
            url = f"{self.telegram_url}/{method}"
            params = {'offset': self.offset}
            resp = requests.get(url, params=params)

            resp_json = json.loads(resp.text)

            handlers = []

            if resp_json['result']:
                for message in resp_json['result']:
                    try:
                        chat_id = message["message"]["chat"]["id"]
                        text = message["message"]["text"]
                        handlers.append(Thread(target=self.message_handle, args=(chat_id, text, )))
                        self.logger.info(f"Chat id: {chat_id} text: {text}")
                    except Exception as e:
                        self.logger.warning(f"Message skipped due to -> {e}")

                self.offset = resp_json['result'][-1]['update_id'] + 1

                [h.start() for h in handlers]

            else:
                self.logger.info("No new messages")

            time.sleep(1)

    def message_handle(self, chat_id, text):
        if text == '/start':
            self.send_message(chat_id, text="Привет! Напишите любой текст, чтобы начать заказывать пиццу. Если захотите прервать диалог напишите \"Выход\"")
        else:
            if chat_id not in self.clients:
                self.clients[chat_id] = Pizza(self)                     # Only pizza intent
            client_intent = self.clients.get(chat_id)
            client_intent.next(chat_id=chat_id, text=text)

    def receive_message(self):

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
