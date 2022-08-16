import telebot
import psycopg2
import src

from config import host, user, password, db_name, bot_token
from telebot import types

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
    COMMANDS = {'create': src.bot_module.NoteCreating(), 'read_all': src.bot_module.ReadingAll(), 'read_month': src.bot_module.ReadingMonth(), 'read_day': src.bot_module.ReadingDay()}

    @bot.message_handler(commands=['start'])
    def start_shell(message):
        src.bot_module.start(message, bot)

    @bot.callback_query_handler(func = lambda call: True)
    def answer(call):
        list_id = [call.message.chat.id]
        user_id = ' '.join([str(elem) for elem in list_id])

        if isinstance(int(user_id), int) == True:
            user_id = int(user_id)
            bot_command = COMMANDS[call.data]
            bot_command.execute(bot, call.message, cursor, user_id)
        else:
            bot.send_message(call.message.chat.id, 'Ошибка: пользователь не найден')
            start_shell(call.message)

    bot.polling()

if __name__ == "__main__":
    main()