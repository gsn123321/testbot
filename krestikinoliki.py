import telebot
import os
import re
from dotenv import load_dotenv
from telebot import types
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from telebot.states import State, StatesGroup
import random

load_dotenv()



TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Token not found')
    exit()

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(TOKEN, state_storage=state_storage)

bot.add_custom_filter(custom_filter=custom_filters.StateFilter(bot))

board = ['  ', '  ', '  ',
         '  ', '  ', '  ',
         '  ', '  ', '  ',]

player = 'X'
bot_player = 'O'


def keyboard():

    k = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(board[0], callback_data='0')
    b2 = types.InlineKeyboardButton(board[1], callback_data='1')
    b3 = types.InlineKeyboardButton(board[2], callback_data='2')

    b4 = types.InlineKeyboardButton(board[3], callback_data='3')
    b5 = types.InlineKeyboardButton(board[4], callback_data='4')
    b6 = types.InlineKeyboardButton(board[5], callback_data='5')

    b7 = types.InlineKeyboardButton(board[6], callback_data='6')
    b8 = types.InlineKeyboardButton(board[7], callback_data='7')
    b9 = types.InlineKeyboardButton(board[8], callback_data='8')

    k.row(b1, b2, b3)
    k.row(b4, b5, b6)
    k.row(b7, b8, b9)

    return k

def win(s):

    if board[0] == s and board[1] == s and board[2] == s:
        return True

    if board[3] == s and board[4] == s and board[5] == s:
        return True

    if board[6] == s and board[7] == s and board[8] == s:
        return True

    if board[0] == s and board[3] == s and board[6] == s:
        return True

    if board[1] == s and board[4] == s and board[7] == s:
        return True

    if board[2] == s and board[5] == s and board[8] == s:
        return True

    if board[0] == s and board[4] == s and board[8] == s:
        return True

    if board[2] == s and board[4] == s and board[6] == s:
        return True



@bot.message_handler(commands=['start'])
def start(message):

    global board

    board = ['  ', '  ', '  ',
             '  ', '  ', '  ',
             '  ', '  ', '  ']

    k = types.InlineKeyboardMarkup()

    x = types.InlineKeyboardButton(
        'Грати за x',
        callback_data='x'
    )

    o = types.InlineKeyboardButton(
        'Грати за o',
        callback_data='o'
    )

    k.row(x, o)

    bot.send_message(
        message.chat.id,
        'Оберите символ',
        reply_markup=k
    )

@bot.callback_query_handler(func=lambda call: call.data == 'x' or call.data == 'o')
def choose(call):

    global player
    global bot_player

    if call.data == 'x':
        player = 'X'
        bot_player = 'O'

    else:
        player = 'O'
        bot_player = 'X'

    bot.edit_message_text(
        'Гра почалась',
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def game(call):

    n = int(call.data)

    if board[n] != '  ':
        return

    board[n] = player

    if win(player):

        bot.edit_message_text(
            'Ви переміг',
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard(),
        )

        return


    if '  ' not in board:

        bot.edit_message_text(
            'Нічия',
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard(),
        )

        return

    empty = []

    for i in range(9):

        if board[i] == '  ':
            empty.append(i)

    bot_move = random.choice(empty)

    board[bot_move] = bot_player

    if win(bot_player):

        bot.edit_message_text(
            'Бот переміг',
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard(),
        )

        return

    bot.edit_message_text(
        'Ваш хід',
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard()
    )


if __name__ == '__main__':
    print('Bot is running....')
    bot.infinity_polling()










