import argparse
import os
from yaml import load, FullLoader
from flask import Flask
from src.api import Api
from src.api.telegram import Telegram
from src.api.vk import Vk
from src.api.facebook import Facebook
from src.utils.logger import Logger


class Bot:
    """
    Bot class implement simple flask server and messengers api registration
    """
    def __init__(self):
        self.logger = Logger().get()    # Logger singleton
        self.app = Flask(__name__)      # Flask app

    def get_app(self):
        """
        App getter
        :return:
        """
        return self.app

    def start(self, host, port):
        """
        Running flask server
        :param host: host
        :param port: port
        :return:
        """
        self.app.run(host=host, port=port)

    def register(self, api: Api):
        """
        Register api webhook(depends on api realization)
        :param api: Api instance
        :return:
        """
        api.register(self.get_app())


if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="pizza bot")
    parser.add_argument('-c', '--config', type=str, action='store', help='bot config yaml file', default='config.yaml')
    args = parser.parse_args()
    config = args.config

    if not os.path.exists(config):
        raise FileNotFoundError(f"Config file is not found on: {config}")

    # Reading config file
    with open(config, encoding='utf-8') as file:
        config = load(file, Loader=FullLoader)

    bot = Bot()

    apis = [
        Telegram(
            token=config['messengers']['telegram']['token'],
            api=config['messengers']['telegram']['api'],
            webhook=config['messengers']['telegram']['webhook'],
        ),
        # Vk(app=bot.get_app()),
        # Facebook(app=bot.get_app())
    ]

    # Api registration
    for messenger_api in apis:
        bot.register(messenger_api)

    # Running flask server
    bot.start(host=config['bot']['host'], port=os.environ.get("PORT", config['bot']['port']))   # Get heroku port from env
