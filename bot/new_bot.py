import requests
import telebot
import json
from token_bot import token
from datetime import datetime
from telebot import types
from api_belarusbank import get_exchange_rates
global text_us

def get_exchange_rates_conversion(currencies: list, direstion: str, city: str) -> str:
    result = ''
    for currency in currencies:
        s = requests.Session()
        r = s.get(f'https://belarusbank.by/api/kursExchange?city={city.title()}')
        r = json.loads(r.text)
        result += f'{currency.upper()}: {r[0][f"{currency.upper()}_{direstion.lower()}"]} \n'
    return result

if __name__ == '__main__':
    get_exchange_rates_conversion(['usd_eur', 'usd_rub', 'rub_eur'], 'out', 'минск')
    get_exchange_rates_conversion(['usd_eur', 'usd_rub', 'rub_eur'], 'in', 'минск')


def get_exchange_rates(currencies: list, direstion: str, city: str) -> str:
    result = ''
    for currency in currencies:
        s = requests.Session()
        r = s.get(f'https://belarusbank.by/api/kursExchange?city={city.title()}')
        r = json.loads(r.text)
        result += f'{currency.upper()}: {r[0][f"{currency.upper()}_{direstion.lower()}"]} \n'
    return result

if __name__ == '__main__':
    get_exchange_rates(['usd', 'eur', 'rub'], 'out', 'минск')
    get_exchange_rates(['usd', 'eur', 'rub'], 'in', 'минск')

def telegram_bot(token):
    bot = telebot.TeleBot(token)
    @bot.message_handler(commands=['start'])
    def start_message(message):
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Курс', 'Конвертер')
        bot.send_message(message.chat.id, 'Приветствую тебя !', reply_markup=keyboard)

    @bot.message_handler(content_types=['text'],func=lambda message: True)
    def exchange_rates(message):
        if message.text == 'Курс':
            bot.send_message(message.chat.id, f"Покупка:\n{get_exchange_rates(['usd', 'eur', 'rub'], 'in', 'минск')}")
            bot.send_message(message.chat.id, f"Продажа:\n{get_exchange_rates(['usd', 'eur', 'rub'], 'out', 'минск')}")
            bot.send_message(message.chat.id, f"Покупка:\n{get_exchange_rates_conversion(['usd_eur', 'usd_rub', 'rub_eur'], 'in', 'минск')}")
            bot.send_message(message.chat.id, f"Продажа:\n{get_exchange_rates_conversion(['usd_eur', 'usd_rub', 'rub_eur'], 'out', 'минск')}")
        elif message.text == 'Конвертер':

            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('USD', 'EUR', 'RUB')
            bot.send_message(message.chat.id, 'какую валюты ту хочешь конвертировать?', reply_markup=keyboard)
        elif message.text == 'USD':
            bot.send_message(message.chat.id, 'Введите сумму целочисленную')

            if message.text == '1234567890':
                text_us = message.text
                usd = get_exchange_rates(['usd'], 'out', 'минск').split()
                usd = float(usd[1])
                text_us_int = text_us
            # usd_con = text_us_int / usd
            # usd_con = str(usd_con)
                bot.reply_to(message, text_us)



    bot.polling()



if __name__ == "__main__":
    telegram_bot(token),
