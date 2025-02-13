import telebot
import json

def send_notifty(message):
    with open("config.json") as config:
        config_data = json.load(config)
        bot_token = config_data["BOT_TOKEN"]
    bot = telebot.TeleBot(bot_token)
    bot.send_message(5719110839, message)