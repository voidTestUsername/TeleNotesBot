import telebot
import psycopg2
import datetime

from config import host, user, password, db_name, bot_token
from telebot import types

bot = telebot.TeleBot(bot_token)

connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )

@bot.message_handler(commands=['start'])
def start(message):
    markup_inline = types.InlineKeyboardMarkup()
    new_note = types.InlineKeyboardButton(text = 'Новая заметка', callback_data = 'create')
    all_notes = types.InlineKeyboardButton(text = 'Все заметки', callback_data = 'read_all')
    month_notes = types.InlineKeyboardButton(text = 'Заметки за месяц', callback_data = 'read_month')
    day_notes = types.InlineKeyboardButton(text = 'Заметки за день', callback_data = 'read_day')

    markup_inline.add(new_note)
    markup_inline.add(all_notes)
    markup_inline.add(month_notes)
    markup_inline.add(day_notes)
    bot.send_message(message.chat.id, 'Меню', reply_markup = markup_inline)

@bot.callback_query_handler(func = lambda call: True)
def bot_answer(call):

    cursor = connection.cursor()

    connection.autocommit = True

    list_id = [call.message.chat.id]
    user_id = ' '.join([str(elem) for elem in list_id])

    if isinstance(int(user_id), int) == True:

        user_id = int(user_id)

        if call.data == 'create':
            msg = bot.send_message(call.message.chat.id, 'Отправьте текст заметки')
        
            def get_note(message):
                msg_text = str(message.text)
                msg_date = str(datetime.datetime.now())
                cursor.execute("INSERT INTO notes (user_id, note_text, note_date) VALUES (%d, '%s', '%s')" %(user_id, msg_text, msg_date))
                bot.send_message(message.chat.id, 'Запись успешно сохранена!')
                start(call.message)
            bot.register_next_step_handler(msg, get_note)

        elif call.data == 'read_all':
            cursor.execute("SELECT note_text, TO_CHAR(note_date, 'YYYY-MM-DD \nhh:mm') FROM notes WHERE user_id = %d" %(user_id))
            answer = ''
            for col in cursor.fetchall():
                answer += str(col[1]) + '\n\n' + str(col[0]) + '\n\n\n\n'
            bot.send_message(call.message.chat.id, answer)
            start(call.message)

        elif call.data == 'read_month':
            msg = bot.send_message(call.message.chat.id, 'Введите месяц и год в формате гггг-мм')
        
            def get_month(message):
                msg_month = str(message.text)
                try:
                    cursor.execute("SELECT note_text, note_date FROM notes WHERE user_id = %d AND TO_CHAR(note_date, 'YYYY-MM') LIKE '%s'" %(user_id, msg_month))
                    month_answer = ''
                    for month_col in cursor.fetchall():
                        month_answer += str(month_col[1].strftime("%Y-%m-%d \n%H:%M")) + '\n\n' + str(month_col[0]) + '\n\n\n\n'
                    bot.send_message(call.message.chat.id, month_answer)
                except:
                    bot.send_message(message.chat.id, 'Ошибка: данные не обнаружены')
                start(call.message)
            bot.register_next_step_handler(msg, get_month)

        elif call.data == 'read_day':
            msg = bot.send_message(call.message.chat.id, 'Введите дату в формате гггг-мм-дд')
        
            def get_day(message):
                msg_day = str(message.text)
                cursor.execute("SELECT note_text, note_date FROM notes WHERE user_id = %d AND TO_CHAR(note_date, 'YYYY-MM-DD') LIKE '%s'" %(user_id, msg_day))
                day_answer = msg_day + '\n\n'
                day_get = False
                for day_col in cursor.fetchall():
                    day_get = True
                    day_answer += str(day_col[1].strftime("%H:%M")) + '\n\n' + str(day_col[0]) + '\n\n\n\n'
                if day_get == True:
                    bot.send_message(call.message.chat.id, day_answer)
                else:
                    bot.send_message(message.chat.id, 'Ошибка: данные не обнаружены')
                start(call.message)
            bot.register_next_step_handler(msg, get_day)
    else:
        bot.send_message(message.chat.id, 'Ошибка: пользователь не найден')
        start(call.message)

bot.polling()