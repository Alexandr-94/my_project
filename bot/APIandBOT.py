import requests
import telebot
import json
from token_bot import token
from datetime import datetime
from telebot import types
from api_belarusbank import get_exchange_rates
# API беларусьбанка.
def get_exchange_rates_conversion(currencies: list, direstion: str, city: str) -> str:
    result = ''
    for currency in currencies:
        s = requests.Session()
        r = s.get(f'https://belarusbank.by/api/kursExchange?city={city.title()}')
        r = json.loads(r.text)
        result += f'{currency.upper()}: {r[0][f"{currency.upper()}_{direstion.lower()}"]} \n'
    return result
# берем необходимую нам конверсию валюты и указываем покупку или продажу.
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
# берем необходимую нам валюту и указываем покупку или продажу.
if __name__ == '__main__':
    get_exchange_rates(['usd', 'eur', 'rub'], 'out', 'минск')
    get_exchange_rates(['usd', 'eur', 'rub'], 'in', 'минск')

# Активация бота.
def telegram_bot(token):
    bot = telebot.TeleBot(token)
    # создаем кнопки.
    @bot.message_handler(commands=['start'])
    def hello_bot(message):
        bot.send_message(message.from_user.id, "Приветствую мой друг")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Да', 'Нет')
        bot.send_message(message.chat.id, 'Тебя интерует курс валют?', reply_markup=keyboard)
    # условия по курсам.
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):

        if message.text == "Да":
            bot.send_message(message.from_user.id, "Что тебя интересует?")
            keyboard = types.InlineKeyboardMarkup()
            #
            buy = types.InlineKeyboardButton(text='Покупка', callback_data='currency_buy')
            keyboard.add(buy)
            sale = types.InlineKeyboardButton(text='Продажа', callback_data='currency_sale')
            keyboard.add(sale)
            sale = types.InlineKeyboardButton(text='Конверсия', callback_data='currency_conversion')
            keyboard.add(sale)
            bot.send_message(message.from_user.id, text='Выбери', reply_markup=keyboard)
        elif message.text == "Нет":
            bot.send_message(message.from_user.id, "Ну смотри если что пиши!")
        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Ну что ты вот начинаешь то ?? нормальноже общались!! "
                                                   "слушай если тебе надо курс валют то нажми на кнопку "
                                                   "<Курс> или напиши в сообщении, а если ничего не надо то так же "
                                                   "выбери кнопку <Ничего> или напиши в сообщении,"
                                                   "ей-богу как маленький!")
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    # логика обработки по нажатию на пнопки
    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):

        if call.data == "currency_buy":
            bot.send_message(call.message.chat.id, f"Покупка:\n{get_exchange_rates(['usd', 'eur', 'rub'], 'in', 'минск')}")
        elif call.data == "currency_sale":
            bot.send_message(call.message.chat.id, f"Продажа:\n{get_exchange_rates(['usd', 'eur', 'rub'], 'out', 'минск')}")
        elif call.data == "currency_conversion":
            bot.send_message(call.message.chat.id, f"Покупка:\n{get_exchange_rates_conversion(['usd_eur', 'usd_rub', 'rub_eur'], 'in', 'минск')}")
            bot.send_message(call.message.chat.id, f"Продажа:\n{get_exchange_rates_conversion(['usd_eur', 'usd_rub', 'rub_eur'], 'out', 'минск')}")
    bot.polling()



if __name__ == "__main__":
    telegram_bot(token),
