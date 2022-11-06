# Калькулятор арифметических выражений

import telebot
from telebot import types
import logging

TOKEN = ''
user_id = 0

f_expr = False # Флаг вычисления выражения

# Вычислить выражение
def calc_expr(in_str: str):
    tuple_valid = {'0', '1', '2', '3', '4', '5', '6', '7',
                   '8', '9', '(', ')', '+', '-', '*', '/', '.', 'j', ' '}
    if not [s for s in list(in_str) if not (s in tuple_valid)]:
        try:
            return eval(in_str)
        except:
            return 'Ошибка в выражении. Не может быть вычислено'
    else:
        return 'Недопустимые символы в выражении'

 
def menu_show(mess):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4) #создание новых кнопок
    btn1 = types.KeyboardButton('Начать работу')
    btn2 = types.KeyboardButton('Помочь вам')
    btn3 = types.KeyboardButton('Вычислить')
    btn4 = types.KeyboardButton('Закончить работу')
    markup.add(btn1, btn2, btn3)
    bot.send_message(mess.from_user.id, 'Что нужно сделать❓', reply_markup=markup) #ответ бота

def bot_help(mess):
    logging.info(f'{mess.from_user.id} вызвал "Помочь вам"')
    help_text = ('Привет! \n'  +  'Это калькулятор арифметических выражений:\n' +
                'Калькулятор вычисляет любые арифметические выражения, включая комплексные числа\n' 
                "В выражении допускаются только символы 0 1 2 3 4 5 6 7 8 9 ( ) * / + - . j пробел\n" +
                'Выражение должно быть правильным с точки зрения языка Python\n'
                )
    bot.send_message(mess.from_user.id, help_text)

def bot_expr(mess):        
    global f_expr
    logging.info(f'{mess.from_user.id} вызвал "Вычисление выражения {mess.text}"')
    expr_val = mess.text
    res = calc_expr(expr_val)
    bot.send_message(mess.from_user.id, res)
    f_expr = False        
    menu_show(mess)

# Включаем протоколирование действий 
logging.basicConfig(format = "%(asctime)s - %(levelname)s - %(message)s", 
                    level = logging.INFO, 
                    filename = "bot.log", 
                    filemode = "w",
                    encoding='utf-8'
                    )

bot = telebot.TeleBot(TOKEN) # Создаем бота

@bot.message_handler(commands=['start']) # Обработчик команды start
def start(message):
    menu_show(message)
    
@bot.message_handler(content_types=['text']) # Обработчик текста входящего сообщения
def get_text_messages(message):
    global f_expr
    if f_expr:
        bot_expr(message)        
    
    elif message.text == '👋 Поздороваться':
        logging.info(f'{message.from_user.id} вызвал "👋 Поздороваться"')
        menu_show(message)

    elif message.text == 'Помочь вам':
        bot_help(message)
        
    elif message.text == 'Вычислить':
        logging.info(f'{message.from_user.id} вызвал "Вычислить"')
        f_expr = True
        bot.send_message(message.from_user.id, 'Введите выражение для вычисления')

    elif message.text == 'Закончить работу':
        logging.info(f'{message.from_user.id} вызвал "Закончить работу"')
        f_expr = True
        bot.send_message(message.from_user.id, 'Досвидания!')
        bot.stop_bot()

    elif message.text == 'Начать работу':
        logging.info(f'{message.from_user.id} вызвал "Начать работу"')
        f_expr = True
        start(message)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("👋 Поздороваться")
markup.add(btn1)
bot.send_message(user_id, "👋 Привет! Я твой бот-калькулятор арифметических выражений!", reply_markup=markup)

logging.info('Start bot')
bot.polling(none_stop=True, interval=0) # Запуск прослушивания очереди
