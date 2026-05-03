import telebot
import os
import re
from dotenv import load_dotenv
from telebot import types
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from telebot.states import State, StatesGroup


load_dotenv()



TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Tokrn not found')
    exit()

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(TOKEN, state_storage=state_storage)

bot.add_custom_filter(custom_filter=custom_filters.StateFilter(bot))

class RegistrationStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_phone = State()

reg_kb = types.ReplyKeyboardMarkup()
reg_btn = types.KeyboardButton('Реєстрація')
reg_kb.add(reg_btn)

cansel_kb = types.InlineKeyboardMarkup()
cansel_btn = types.InlineKeyboardButton('Скасувати', callback_data='cansel')
cansel_kb.add(cansel_btn)

remove_kb = types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(
        message.chat.id,
        'Hi! Press the button!',
        reply_markup=reg_kb
    )



@bot.message_handler (func=lambda message: message.text.startswith("Реєстрація"))
def start_reg(message):
    temp_msg = bot.send_message(
        message.chat.id,
        'Оновляємо інтерфейс....',
        reply_markup=remove_kb
    )

    bot.delete_message(message.chat.id, temp_msg.id)

    bot.set_state(
        message.from_user.id,
        RegistrationStates.waiting_for_email,
        message.chat.id,
        )

    bot.set_state(
        message.from_user.id,
        RegistrationStates.waiting_for_phone,
        message.chat.id,
        )
    
    bot.send_message(
        message.chat.id,
        "Чудово! Надішли мені адресу електроної пошти або нмоер телефону, на яку хочеш отримувати спам!",
        reply_markup=cansel_kb
    )

@bot.message_handler(state=RegistrationStates.waiting_for_email)
def process_email(message):
    email = message.text
    email_pattern = r'^[\w\.-_]+@[\w\.-_]+\.\w+\$'

    if re.match(email_pattern, email):
        print(f'New email: {email}')
        
        with open('emails.txt', '+a') as file:
            file.write(email + '\n')

        bot.delete_state(message.from_user.id, message.chat.id)

        bot.send_message(
            message.chat.id,
            'Дякую',
            reply_markup=reg_kb,
        )
    else: 
        bot.send_message(
            message.chat.id,
            'Не схоже на Email',
        )

@bot.message_handler(state=RegistrationStates.waiting_for_phone)
def process_phone(message):
    phone = message.text
    pattern = r'^\+380\d{9}$'

    if re.match(pattern, phone):
        print(f'New phone: {phone}')

        with open('emails.txt', '+a') as file:
            file.write(phone + '\n')

        bot.delete_state(message.from_user.id, message.chat.id)

        bot.send_message(
            message.chat.id,
            'Дякую',
            reply_markup=reg_kb,
        )
    else: 
        bot.send_message(
            message.chat.id,
            'Не схоже на телефон',
        )
    

@bot.callback_query_handler(func=lambda call: call.data == 'cansel')
def cansel_handler(call):
    bot.delete_state(call.from_user.id, call.message.chat.id)
    bot.send_message(
        call.message.chat.id,
        'Якщо передумаєш натисни "Реєстрація" знову.',
        reply_markup=reg_kb
    )
    bot.answer_callback_query(call.id)

if __name__ == '__main__':
    print('Bot is running....')
    bot.infinity_polling()







