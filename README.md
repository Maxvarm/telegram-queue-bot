# Telegram Queue Bot

A small bot for creating customizable queues in groups written in Python. Using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) as Telegram API wrapper and [mongoengine](https://github.com/MongoEngine/mongoengine) as ODM for MongoDB.

## Installation

Using venv:

```bash
sudo apt install python3-venv
source start.sh
```

## Usage

Get token from [@BotFather](https://telegram.me/BotFather) and set following settings:
```bash
/setinline
/setinlinefeedback
```
Then configure MongoDB and private.py file
```python3
telegram_token = "token from father bot"
db_name = "chosen database name"
db_host = "localhost"
```
Run bot
```bash
python3 bot.py
```
In Telegram, start the bot and type *@BotName 'Queue-title(Optional)'*, wait for inline answer to load and customize the queue!