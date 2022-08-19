import telebot
import psycopg2
import src.bot_module

from config import host, user, password, db_name, bot_token

bot = telebot.TeleBot(bot_token)

connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
cursor = connection.cursor()
connection.autocommit = True

def main():

    COMMANDS = {'create': src.NoteCreating(), 'read_all': src.ReadingAll(),
                'read_month': src.ReadingMonth(), 'read_day': src.ReadingDay(),
                'download_txt': src.DownloadingNote()}

    @bot.message_handler(commands=['start'])
    def start_shell(message):
        src.start(message, bot, '0')

    @bot.message_handler(regexp='дневник')
    def start_shell2(message):
        list_id = [message.chat.id]
        user_id = ' '.join([str(elem) for elem in list_id])

        if isinstance(int(user_id), int) == True:
            user_id = int(user_id)
            bot_command = bot_module.NoteCreating()
            bot_command.execute(bot, message, cursor, user_id)
        else:
            bot.send_message(message.chat.id, 'Ошибка: пользователь не найден')
            start_shell(message)

    @bot.callback_query_handler(func = lambda call: True)
    def answer(call):
        list_id = [call.message.chat.id]
        user_id = ' '.join([str(elem) for elem in list_id])

        if isinstance(int(user_id), int) == True:
            user_id = int(user_id)
            bot_command = COMMANDS[call.data]

            if not isinstance(bot_command, src.DownloadingNote):
                bot_command.execute(bot, call.message, cursor, user_id)
            else:
                filename = bot_command.saved_text.split('\n')[0]
                bot_command.execute_special(bot, call.message, filename, bot_command.saved_text)
        else:
            bot.send_message(call.message.chat.id, 'Ошибка: пользователь не найден')
            start_shell(call.message)

    bot.polling()

if __name__ == "__main__":
    main()