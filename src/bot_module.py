from telebot import types
import datetime

class Bot_Command():
    def execute(self):
        raise(NotImplementedError)

def start(message, bot):
    markup_inline = types.InlineKeyboardMarkup()
    new_note = types.InlineKeyboardButton(text='Новая заметка', callback_data='create')
    all_notes = types.InlineKeyboardButton(text='Все заметки', callback_data='read_all')
    month_notes = types.InlineKeyboardButton(text='Заметки за месяц', callback_data='read_month')
    day_notes = types.InlineKeyboardButton(text='Заметки за день', callback_data='read_day')
    markup_inline.add(new_note)
    markup_inline.add(all_notes)
    markup_inline.add(month_notes)
    markup_inline.add(day_notes)

    bot.send_message(message.chat.id, 'Меню', reply_markup=markup_inline)

class NoteCreating(Bot_Command):
    def execute(self, bot, message, cursor, user_id):
        msg = bot.send_message(message.chat.id, 'Отправьте текст заметки')
        def get_note(message):
            msg_text = str(message.text)
            msg_date = str(datetime.datetime.now())
            cursor.execute("INSERT INTO notes (user_id, note_text, note_date) VALUES (%d, '%s', '%s')" %(user_id, msg_text, msg_date))
            bot.send_message(message.chat.id, 'Запись успешно сохранена!')
            start(message, bot)
        bot.register_next_step_handler(msg, get_note)

class ReadingAll(Bot_Command):
    def execute(self, bot, message, cursor, user_id):
        cursor.execute("SELECT note_text, TO_CHAR(note_date, 'YYYY-MM-DD \nhh:mm') FROM notes WHERE user_id = %d ORDER BY note_date" %(user_id))
        answer = ''
        for col in cursor.fetchall():
            answer += str(col[1]) + '\n\n' + str(col[0]) + '\n\n\n\n'
        bot.send_message(message.chat.id, answer)
        start(message, bot)

class ReadingMonth(Bot_Command):
    def execute(self, bot, message, cursor, user_id):
        msg = bot.send_message(message.chat.id, 'Введите месяц и год в формате гггг-мм')
        def get_month(message):
            msg_month = str(message.text)
            try:
                cursor.execute("SELECT note_text, note_date FROM notes WHERE user_id = %d AND TO_CHAR(note_date, 'YYYY-MM') LIKE '%s'  ORDER BY note_date" %(user_id, msg_month))
                month_answer = ''
                for month_col in cursor.fetchall():
                    month_answer += str(month_col[1].strftime("%Y-%m-%d \n%H:%M")) + '\n\n' + str(month_col[0]) + '\n\n\n\n'
                bot.send_message(message.chat.id, month_answer)
            except:
                bot.send_message(message.chat.id, 'Ошибка: данные не обнаружены')
            start(message, bot)
        bot.register_next_step_handler(msg, get_month)

class ReadingDay(Bot_Command):
    def execute(self, bot, message, cursor, user_id):
        msg = bot.send_message(message.chat.id, 'Введите дату в формате гггг-мм-дд')
        def get_day(message):
            msg_day = str(message.text)
            cursor.execute("SELECT note_text, note_date FROM notes WHERE user_id = %d AND TO_CHAR(note_date, 'YYYY-MM-DD') LIKE '%s' ORDER BY note_date" %(user_id, msg_day))
            day_answer = msg_day + '\n\n'
            day = False
            for day_col in cursor.fetchall():
                day = True
                day_answer += str(day_col[1].strftime("%H:%M")) + '\n\n' + str(day_col[0]) + '\n\n\n\n'
            if day == True:
                bot.send_message(message.chat.id, day_answer)
            else:
                bot.send_message(message.chat.id, 'Ошибка: данные не обнаружены')
            start(message, bot)
        bot.register_next_step_handler(msg, get_day)
