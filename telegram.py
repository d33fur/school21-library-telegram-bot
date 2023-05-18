# -*- coding: utf-8 -*-

import telebot
from telebot import types
from database.dbapi import DatabaseConnector
memory = {}
token = ""
bot = telebot.TeleBot(token)

db_connector = DatabaseConnector(db_name="bookworm")


@bot.message_handler(commands=['start'])# Стартовая функция
def handle_start(message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("/add")
    button2 = types.KeyboardButton("/delete")
    button3 = types.KeyboardButton("/list")
    button4 = types.KeyboardButton("/find")
    button5 = types.KeyboardButton("/borrow")
    button6 = types.KeyboardButton("/retrieve")
    button7 = types.KeyboardButton("/stats")
    buttons.add(button1, button2, button3, button4, button5, button6, button7)
    bot.send_message(message.chat.id, "Добро пожаловать в чат бота-библиотеки!", reply_markup=buttons)


@bot.message_handler(commands=['add', 'delete', 'list', 'find', 'borrow', 'retrieve', 'stats'])
def handle_start(message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_stop = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("/add")
    button2 = types.KeyboardButton("/delete")
    button3 = types.KeyboardButton("/list")
    button4 = types.KeyboardButton("/find")
    button5 = types.KeyboardButton("/borrow")
    button6 = types.KeyboardButton("/retrieve")
    button7 = types.KeyboardButton("/stats")
    button_stop = types.KeyboardButton("/stop")
    buttons_stop.add(button_stop)
    buttons.add(button1, button2, button3, button4, button5, button6, button7)
    #buttons0 = telebot.types.ReplyKeyboardRemove()

    memory[f'{message.chat.id}'] = []
    memory[f'{message.chat.id}'].append(message.text)
    print(memory) # проверка

    command = memory[f'{message.chat.id}'][0]

    if(command == "/add" or command == '/delete'
            or command == '/find' or command == '/borrow'
            or command == '/stats'):
        temp = len(memory[f'{message.chat.id}'])
        for i in range(1, temp):
            memory[f'{message.chat.id}'].pop()
        bot.send_message(message.chat.id, "Введите название книги:", reply_markup=buttons_stop)
        bot.register_next_step_handler(message, enter_book_name)

    elif(command == "/list"):
        try:
            temp = db_connector.list_books()
            for i in range(0, len(temp)):
                bot.send_message(message.chat.id, f"{temp[i]};")
            bot.send_message(message.chat.id, "На этом все.", reply_markup=buttons)

        except:
            bot.send_message(message.chat.id,"Ошибка при выдаче списка книг.", reply_markup=buttons)

    elif(command == "/retrieve"):
        user_id = message.chat.id
        try:
            temp = db_connector.retrieve(user_id)

            if(temp):
                bot.send_message(message.chat.id, f"Вы вернули книгу {temp}.", reply_markup=buttons)
            else:
                bot.send_message(message.chat.id, "Не получилось вернуть книгу.", reply_markup=buttons)

        except:
            bot.send_message(message.chat.id, "Ошибка при возврате книги.", reply_markup=buttons)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда.")



def enter_book_name(message):
    if(message.text == '/stop'):
        stop(message)

    else:
        buttons_stop = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_stop = types.KeyboardButton("/stop")
        buttons_stop.add(button_stop)
        memory[f'{message.chat.id}'].append(message.text)
        bot.send_message(message.chat.id, "Введите автора:", reply_markup=buttons_stop)
        bot.register_next_step_handler(message, enter_author_name)


def enter_author_name(message):
    if(message.text == '/stop'):
        stop(message)

    else:
        buttons_stop = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_stop = types.KeyboardButton("/stop")
        buttons_stop.add(button_stop)
        memory[f'{message.chat.id}'].append(message.text)
        bot.send_message(message.chat.id, "Введите год издания:", reply_markup=buttons_stop)
        bot.register_next_step_handler(message, enter_year_of_publishing)


def enter_year_of_publishing(message):
    if(message.text == '/stop'):
        stop(message)

    else:
        buttons0 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button11 = types.KeyboardButton("Да")
        button22 = types.KeyboardButton("Нет")
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("/add")
        button2 = types.KeyboardButton("/delete")
        button3 = types.KeyboardButton("/list")
        button4 = types.KeyboardButton("/find")
        button5 = types.KeyboardButton("/borrow")
        button6 = types.KeyboardButton("/retrieve")
        button7 = types.KeyboardButton("/stats")
        buttons.add(button1, button2, button3, button4, button5, button6, button7)
        buttons0.add(button11, button22)

        command = memory[f'{message.chat.id}'][0]

        if(message.text.isdigit()):
            memory[f'{message.chat.id}'].append(int(message.text))
            try:
                user_data = memory[f'{message.chat.id}'][1:] # everything except command
                book = db_connector.get_book(title=user_data[0], author=user_data[1], published=int(user_data[2]))

                if(command == "/add"):
                    added_book_id = db_connector.add(title=user_data[0], author=user_data[1], published=int(user_data[2]))

                    if(str(added_book_id).isdigit()):
                        bot.send_message(message.chat.id, f"Книга добавлена ({added_book_id}).", reply_markup=buttons)
                        print(memory) # проверка
                    else:
                        bot.send_message(message.chat.id, "Ошибка при добавлении книги.", reply_markup=buttons)

                elif(command == "/delete"):
                    if(book != None):
                        bot.send_message(message.chat.id, f"Найдена книга: {book}. Удаляем?", reply_markup=buttons0)
                        bot.register_next_step_handler(message, yes_no)
                    else:
                        bot.send_message(message.chat.id, "Книга не найдена.", reply_markup=buttons)

                elif(command == "/find"):
                    if(book != None):
                        bot.send_message(message.chat.id, f"Найдена книга: {book}.", reply_markup=buttons)
                        print(memory) # проверка
                    else:
                        bot.send_message(message.chat.id, "Такой книги у нас нет.", reply_markup=buttons)

                elif(command == "/stats"):
                    if(book != None):
                        bot.send_message(message.chat.id, f"Статистика доступна по адресу: http://localhost/download/1/{book.book_id}/", reply_markup=buttons)
                        print(memory) # проверка
                    else:
                        bot.send_message(message.chat.id, "Нет такой книги.", reply_markup=buttons)

                elif(command == "/borrow"):
                    if(book != None):
                        bot.send_message(message.chat.id, f"Найдена книга: {book}. Берем?", reply_markup=buttons0)
                        bot.register_next_step_handler(message, yes_no)
                    else:
                        bot.send_message(message.chat.id, "Книга не найдена.", reply_markup=buttons)

            except:
                bot.send_message(message.chat.id, "Ошибка при выполнении (функция).", reply_markup=buttons)


        else:
            bot.send_message(message.chat.id, "Это не число! Введите год издания:")
            bot.register_next_step_handler(message, enter_year_of_publishing)


def yes_no(message):
    if(message.text == '/stop'):
        stop(message)

    else:
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("/add")
        button2 = types.KeyboardButton("/delete")
        button3 = types.KeyboardButton("/list")
        button4 = types.KeyboardButton("/find")
        button5 = types.KeyboardButton("/borrow")
        button6 = types.KeyboardButton("/retrieve")
        button7 = types.KeyboardButton("/stats")
        buttons.add(button1, button2, button3, button4, button5, button6, button7)

        command = memory[f'{message.chat.id}'][0]
        user_data = memory[f'{message.chat.id}'][1:] # everything except command

        if(command == "/delete"):
            if(message.text.lower().capitalize() == "Да"):
                try:
                    temp = db_connector.delete(title=user_data[0], author=user_data[1], published=int(user_data[2]))
                    if(temp):
                        bot.send_message(message.chat.id, "Книга удалена.", reply_markup=buttons)
                        print(memory) # проверка
                    else:
                        bot.send_message(message.chat.id, "Невозможно удалить книгу.", reply_markup=buttons)

                except:
                    bot.send_message(message.chat.id, "Ошибка при удалении книги.", reply_markup=buttons)

            elif(message.text.capitalize() == "Нет"):
                bot.send_message(message.chat.id, "Книга не удалена.", reply_markup=buttons)

        elif(command == "/borrow"):
            if(message.text.capitalize() == "Да"):
                try:
                    temp = db_connector.borrow(title=user_data[0], author=user_data[1], published=int(user_data[2]), user_id=str(message.chat.id))

                    if(temp != False):
                        bot.send_message(message.chat.id, "Вы взяли книгу.", reply_markup=buttons)
                    else:
                        bot.send_message(message.chat.id, "Книгу сейчас невозможно взять.", reply_markup=buttons)

                except:
                    bot.send_message(message.chat.id, "Ошибка при взятии книги.", reply_markup=buttons)

            elif(message.text.capitalize() == "Нет"):
                bot.send_message(message.chat.id, "Вы не взяли книгу.", reply_markup=buttons)

def stop(message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("/add")
    button2 = types.KeyboardButton("/delete")
    button3 = types.KeyboardButton("/list")
    button4 = types.KeyboardButton("/find")
    button5 = types.KeyboardButton("/borrow")
    button6 = types.KeyboardButton("/retrieve")
    button7 = types.KeyboardButton("/stats")
    buttons.add(button1, button2, button3, button4, button5, button6, button7)
    bot.send_message(message.chat.id, "Операция прервана.", reply_markup=buttons)
    bot.register_next_step_handler(message, handle_start)

bot.infinity_polling()
