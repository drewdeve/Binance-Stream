# Binance-Stream

**Binance-Stream** is a Telegram bot that streams data from Binance using websockets, and all data is recorded in the PostegreSQL database.

## How it work?

The user enters the bot's telegram, writes the `/start` command, learns how to start the process, for this you need to add the bot to the group to which the data will be sent. The user can also stop the bot using the `/stop` command.

## How to run the bot?

Downloads this project, you must have Python installed, preferably version 3.9
[Follow the link to learn how to install Python](https://www.tutorialspoint.com/how-to-install-python-in-windows)

Then install all the necessary libraries to work with the project. You can use the requirements.txt file and enter command in the console after which all project libraries will be installed.
```bash
pip install -r requirements.txt
```
[About pip](https://phoenixnap.com/kb/install-pip-windows)

## Run project

You need to run the bot.py file, either through the IDE or through the console `py bot.py`
