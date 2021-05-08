import argparse
import os
from yaml import load, FullLoader
from flask import Flask
from src.api.telegram import Telegram
from src.api.vk import Vk
from src.api.facebook import Facebook
from src.utils.logger import Logger


class Bot:

    def __init__(self):
        self.logger = Logger().get()
        self.app = Flask(__name__)

    def get_app(self):
        return self.app

    def start(self, host, port):
        self.app.run(host=host, port=port)


if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="pizza bot")
    parser.add_argument('-c', '--config', type=str, action='store', help='bot config yaml file', default='config.yaml')
    args = parser.parse_args()
    config = args.config

    if not os.path.exists(config):
        raise FileNotFoundError(f"Config file is not found on: {config}")

    with open(config, encoding='utf-8') as file:
        config = load(file, Loader=FullLoader)

    bot = Bot()

    apis = [
        Telegram(
            token=config['messengers']['telegram']['token'],
            api=config['messengers']['telegram']['api'],
            webhook=config['messengers']['telegram']['webhook'],
            app=bot.get_app()
        ),
        # Vk(app=bot.get_app()),
        # Facebook(app=bot.get_app())
    ]

    for api in apis:
        api.register()

    bot.start(host=config['bot']['host'], port=os.environ.get("PORT", config['bot']['port']))
