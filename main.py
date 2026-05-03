import telebot
import os
from dotenv import load_dotenv
import random
import string
from telebot import types

load_dotenv()



TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Tokrn not found')
    exit()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    sms = bot.send_message(message.chat.id, "Введите число:")
    bot.register_next_step_handler(sms, password)

def password(message):
    if not message.text.isdigit():
        sms = bot.send_message(message.chat.id, "Это не число, еще раз: ")
        bot.register_next_step_handler(sms, password)
    else:
        length = int(message.text)
        symbols = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(symbols) for _ in range(length))
        bot.reply_to(message, password)

@bot.message_handler(commands=['play'])
def start(message):
    sms = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button = types.KeyboardButton("Камінь")
    button2 = types.KeyboardButton("Ножиці")
    button3 = types.KeyboardButton("Бумага")

    sms.add(button, button2, button3)

    bot.send_message(message.chat.id, "Выберите вариант:", reply_markup=sms)

@bot.message_handler(func=lambda message: True)    
def game(message):
    options = ['Камінь', 'Ножиці', 'Бумага']
    comp = random.choice(options)
    if message.text == comp:
        bot.send_message(message.chat.id, f"{message.text} | {comp} Нічия")
    elif message.text == 'Камінь' and comp == 'Ножиці' or message.text == "Ножиці" and comp == "Бумага" or message.text == "Бумага" and comp == "Камінь":
        bot.send_message(message.chat.id, f"{message.text} | {comp} Ви виграли")
    else:
        bot.send_message(message.chat.id, f"{message.text} | {comp} Ви програли")



@bot.message_handler(commands=['info'])
def info_handler(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_name = message.from_user.username
    message_text = message.text

    print(chat_id, user_id, first_name, last_name, user_name, message_text)
    bot.send_message(chat_id, f'Привіт, {first_name}')


@bot.message_handler(func=lambda message: message.text.endswith('?'))
def answer_handler(message):
    answer = ['Да', 'Ні']
    bot.reply_to(message, random.choice(answer))



@bot.message_handler(func=lambda message: True)
def echo_handler(message):
    bot.send_message(message.chat.id, message.text)




if __name__ == '__main__':
    print('Bot is running....')
    bot.infinity_polling()



