# TeleNotesBot
Данный бот служит для автоматизации видения заметок

Инструкция по установке
1. Загрузить дамп в БД
```sh
pg_restore -d [db name] -U [db user] dump_db.sql
```
2. Устновить python 3.10
```sh
apt install python3.10
```
3. Установить необходимые библиотки
```sh
pip install -r requeirements.txt
```
4. Добавить конфигруционный файл в src (config.py), следующего формата
```python
host = "127.0.0.1"
user = "dev"
password = "password"
db_name = "telenotesbot"
bot_token = "5539265970:hjjvodifooisdjfosdifjosdifosjdofj"
```
5. Запустить бота следующей командой
```sh
python src/__main__.py
```

Рекомендуемое ПО для установки:
* Ubuntu 20.04
* Python 3.10.4

Рекомендуемое ПО для разработки:
1. PgAdmin4
2. PyCharm 2022.1.4 

Возможные проблемы при установке:
