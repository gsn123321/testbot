import telebot
import os
from dotenv import load_dotenv

load_dotenv()



TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Tokrn not found')
    exit()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    bot.reply_to(message, 'Привіт, я простий ехо-бот')

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


@bot.message_handler(func=lambda message: message.text.startswith('hello'))
def hello_handler(message):
    bot.reply_to(message, 'Привіт!')



@bot.message_handler(func=lambda message: True)
def echo_handler(message):
    bot.send_message(message.chat.id, message.text)




if __name__ == '__main__':
    print('Bot is running....')
    bot.infinity_polling()



