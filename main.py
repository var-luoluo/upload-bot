import os
import time
import telebot
import logging

BOT_TOKEN = os.environ.get('BOT_TOKEN') # export BOT_TOKEN='your_bot_token_from_@botfather'
FILE_PATH = "" # file path
TO_CHAT = 0 # chat_id, upload to which chat
DELAY_TIME = 2 # after each upload delay 2s

whitelist = []
stop_task_flag = False
record = 0

bot = telebot.TeleBot(BOT_TOKEN)

logging.basicConfig(filename='run.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

# Avoid abused
@bot.message_handler(func=lambda message: message.from_user.id not in whitelist)
def not_in_whitelist(message):
    logging.info(f'user {message.chat.id} try to use bot ...')
    bot.send_message(message.chat.id, "Sorry, you have no privilege on this bot")


@bot.message_handler(commands=['start'])
def start_info(message):
    text = '''Hi
    /start:  Say hello
    /upload: Start upload files from my machine
    '''
    logging.info(f'user {message.chat.id} use /start ...')
    bot.reply_to(message, text, parse_mode="Markdown")


@bot.message_handler(commands=['upload'])
def upload_file(message):
    bot.send_message(message.chat.id, "Uploading")
    logging.info(f'user {message.chat.id} use /upload ...')
    for file_name in os.listdir(FILE_PATH):
        file_path = os.path.join(FILE_PATH, file_name)
        with open(file_path, 'rb') as document:
            msg = bot.send_document(chat_id=TO_CHAT, document=document, disable_notification=True)        
            if msg is None:
                text = f'file {file_path} upload failed!'
                print(text)
                logging.info(text)
                bot.send_message(message.chat.id, text)
                break
            else:
                text = f'file {file_path} upload succeed.'
                print(text)
                logging.info(text)

            # time.sleep(DELAY_TIME) # upload is a consuming task ...
    bot.send_message(message.chat.id, "Finished")
    logging.info(f'upload task finished ...')

    bot.clear_step_handler(message)


bot.infinity_polling()
