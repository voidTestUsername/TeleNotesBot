import telebot
import psycopg2
from bot_module import ReadingAll, NoteCreating, ReadingMonth, ReadingDay, DownloadingNote, menu

from config import host, user as db_user, password, db_name, bot_token

bot = telebot.TeleBot(bot_token)

connection = psycopg2.connect(
    host=host,
    user=db_user,
    password=password,
    database=db_name
)
cursor = connection.cursor()
connection.autocommit = True


def main():
    COMMANDS = {'Новая заметка': NoteCreating(), 'Все заметки': ReadingAll(),
                'Заметки за месяц': ReadingMonth(), 'Заметки за сегодня': ReadingDay(),
                'download_txt': DownloadingNote()}

    @bot.message_handler(commands=['start'])
    def start_shell(message):
        menu(message, bot, '0')

    @bot.message_handler(regexp='(дневник|заметка) (.*)')
    def start_shell2(message):
        list_id = [message.chat.id]
        user_id = ' '.join([str(elem) for elem in list_id]) # Что здесь происходит? Почему нельзя взять просто message.chat.id

        if isinstance(int(user_id), int):
            user_id = int(user_id)
            bot_command = NoteCreating()
            bot_command.execute(bot, message, cursor, user_id)
        else:
            bot.send_message(message.chat.id, 'Ошибка: пользователь не найден') # это сообщение вызвает вопросы
            start_shell(message)

    @bot.message_handler()
    def answer(message):
        list_id = [message.chat.id]
        user_id = ' '.join([str(elem) for elem in list_id]) # Что здесь происходит? Почему нельзя взять просто message.chat.id + дублирование

        if isinstance(int(user_id), int):
            user_id = int(user_id)
            if COMMANDS.__contains__(message.text):
                bot_command = COMMANDS[message.text]

                if not isinstance(bot_command, DownloadingNote):
                    bot_command.execute(bot, message, cursor, user_id)
                else:
                    filename = bot_command.saved_text.split('\n')[0] # есть такое подозрение, что файл будет доступен всем, т.к. у нас всего один экземпляр объекта
                    bot_command.execute_special(bot, message, filename, bot_command.saved_text)
            else:
                bot.send_message(message.chat.id, 'Текст не распознан')
        else:
            bot.send_message(message.chat.id, 'Ошибка: пользователь не найден')
            start_shell(message.text)

    bot.polling(none_stop=True)

    # @bot.callback_query_handler(func=lambda call: True) # тут по идеи должны обрабатываться команды с инлайн кнопок, у нас такая как минимум одна 'скачать text'
    # def answer(call):
    #     bot_command = COMMANDS[call.data]
    #
    #     if not isinstance(bot_command, DownloadingNote):
    #         bot_command.execute(bot, call.message, cursor, call.message.chat.id)
    #     else:
    #         filename = bot_command.saved_text.split('\n')[0]
    #         bot_command.execute_special(bot, call.message, filename, bot_command.saved_text)
    #         start_shell(call.message)
if __name__ == "__main__":
    print("Start work!")
    main()

