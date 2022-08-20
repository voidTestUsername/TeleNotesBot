import telebot
import datetime
import os


class BotCommand:
    saved_text = ' '

    def execute(self):
        raise (NotImplementedError)


def start(message, bot, saved_text):
    markup_inline = telebot.types.InlineKeyboardMarkup()
    new_note = telebot.types.InlineKeyboardButton(text='Новая заметка', callback_data='create')
    all_notes = telebot.types.InlineKeyboardButton(text='Все заметки', callback_data='read_all')
    month_notes = telebot.types.InlineKeyboardButton(text='Заметки за месяц', callback_data='read_month')
    day_notes = telebot.types.InlineKeyboardButton(text='Заметки за сегодня', callback_data='read_day')
    markup_inline.add(new_note)
    markup_inline.add(all_notes)
    markup_inline.add(month_notes)
    markup_inline.add(day_notes)

    if saved_text != '0':
        download_note = telebot.types.InlineKeyboardButton(text='Скачать .txt', callback_data='download_txt')
        markup_inline.add(download_note)

    bot.send_message(message.chat.id, 'Меню', reply_markup=markup_inline)


class NoteCreating(BotCommand):
    def execute(self, bot, message, cursor, user_id):
        msg = bot.send_message(message.chat.id, 'Отправьте текст заметки')

        def get_note(message):
            msg_text = str(message.text)
            msg_date = str(datetime.datetime.now())
            cursor.execute("INSERT INTO notes (user_id, note_text, note_date) VALUES (%d, '%s', '%s')" % (
                user_id, msg_text, msg_date))
            bot.send_message(message.chat.id, 'Запись успешно сохранена!')
            start(message, bot, '0')

        bot.register_next_step_handler(msg, get_note)


class ReadingAll(BotCommand):
    def execute(self, bot, message, cursor, user_id):
        cursor.execute(
            "SELECT note_text, TO_CHAR(note_date, 'YYYY-MM-DD \nhh:mm') FROM notes WHERE user_id = %d ORDER BY note_date" % (
                user_id))
        answer = ''
        for col in cursor.fetchall():
            answer += str(col[1]) + '\n\n' + str(col[0]) + '\n\n\n\n'
        bot.send_message(message.chat.id, answer)
        BotCommand.saved_text = 'Все заметки\n\n' + answer
        start(message, bot, BotCommand.saved_text)


class ReadingMonth(BotCommand):
    def execute(self, bot, message, cursor, user_id):
        msg = bot.send_message(message.chat.id, 'Введите месяц и год в формате гггг-мм')

        def get_month(message):
            msg_month = str(message.text)
            try:
                cursor.execute(
                    "SELECT note_text, note_date FROM notes WHERE user_id = %d AND TO_CHAR(note_date, 'YYYY-MM') LIKE '%s'  ORDER BY note_date" % (
                        user_id, msg_month))
                month_answer = ''
                for month_col in cursor.fetchall():
                    month_answer += str(month_col[1].strftime("%Y-%m-%d \n%H:%M")) + '\n\n' + str(
                        month_col[0]) + '\n\n\n\n'
                BotCommand.saved_text = 'Заметки за ' + message.text + '\n\n' + month_answer
                bot.send_message(message.chat.id, month_answer)
            except:
                BotCommand.saved_text = '0'
                bot.send_message(message.chat.id, 'Ошибка: данные не обнаружены')
            start(message, bot, BotCommand.saved_text)

        bot.register_next_step_handler(msg, get_month)


class ReadingDay(BotCommand):
    def execute(self, bot, message, cursor, user_id):
        cur_date = (str(datetime.datetime.now())).split(' ')[0]
        cursor.execute(
            "SELECT note_text, TO_CHAR(note_date, 'YYYY-MM-DD \nhh:mm') FROM notes WHERE user_id = %d AND TO_CHAR(note_date, 'YYYY-MM-DD') LIKE '%s' ORDER BY note_date" % (
                user_id, cur_date))
        answer = ''
        for col in cursor.fetchall():
            answer += str(col[1]) + '\n\n' + str(col[0]) + '\n\n\n\n'
        bot.send_message(message.chat.id, answer)
        BotCommand.saved_text = 'Заметки за сегодня\n\n' + answer
        start(message, bot, BotCommand.saved_text)


class DownloadingNote(BotCommand):
    def execute_special(self, bot, message, filename, saved_text):
        filename += '.txt'
        data_f = open(filename, 'w', encoding='utf-8')
        data_f.write(saved_text)
        data_f.close()
        bot.send_document(message.chat.id, document=open(filename, 'rb'))
        path = os.path.join(os.path.abspath(os.path.dirname(filename)), filename)
        os.remove(path)
        bot.send_message(message.chat.id, 'Файл готов!')
        start(message, bot, '0')
