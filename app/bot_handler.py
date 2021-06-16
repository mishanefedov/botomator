import requests
import json
import telebot
import time
from django.db import models
import threading
from telegram.ext import Updater,  CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import time
import re
import pyfiglet
import logging
import logging.config
import os
import requests



class BotStarter(threading.Thread):  

  
    def __init__(self, total, api, json):
        self.total = total
        self.api = api
        self.json =json
        threading.Thread.__init__(self)
        
    def get_self(self):
        return self
    
    
    
    def run(self):

        print('FROM_BOT_HANDLER ', self.api)

        request_url = f'https://api.telegram.org/bot{self.api}/getMe'
        r = requests.post(request_url)
        print(r.json())
        print('ACTIVE THREADS COUNT',threading.active_count())
    

        def help_command_handler(update, context):
            """Send a message when the command /help is issued."""
            update.message.reply_text('Type /start')

        def start_command_handler(update, context):
            """Send a message when the command /start is issued."""
            add_typing(update, context)
            buttons = MultiItems("What would you like to receive?", ["Text", "File", "GoogleDoc", "Gallery"])
            add_suggested_actions(update, context, buttons)

        bot = self.total
        api = self.api
        print("alibaba")
        print(DefaultConfig(self.api).TELEGRAM_TOKEN)
        print("alibaba")
        updater = Updater(self.api, use_context=True)
        dp = updater.dispatcher


        dp.add_handler(CommandHandler("help", help_command_handler))
        dp.add_handler(CommandHandler("start", start_command_handler))

        #dp.add_handler(MessageHandler(Filters.text, main_handler))
        # GITHUB
        # https://github.com/gcatanese/TelegramBotDemo/blob/main/telegram_bot/telegram_bot.py
        WEBHOOK_URL = f"https://api.telegram.org/bot{self.api}/setwebhook"
        PORT = 443
        LISTEN = "0.0.0.0"
        
        updater.start_webhook(listen=LISTEN, port=int(PORT), url_path="https://localhost/webhook", webhook_url = WEBHOOK_URL)
        print("SALO")
        #updater.bot.setWebhook(WEBHOOK_URL)

        logging.info(f"Start webhook mode on port {PORT}")
        updater.idle()


class BotStopper(threading.Thread):
    
    def __init__(self, total, api):
        self.total = total
        self.api = api
        threading.Thread.__init__(self)

    
    def run(self):
        bot = self.total
        print('ACTIVE THREADS COUNT',threading.active_count())
        def my_scheduled_job():
    
            try:
                bot.stop_polling()
            except Exception:
                time.sleep(10)
                
        print(f'The bot {self.api} was successfully stopped')
        print('Thread finish')




class DefaultConfig():#models.Model):

    def __init__(self, api):
        self.api = api


    PORT = int(os.environ.get("PORT", 3978))
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKENi", "token be here")
    MODE = os.environ.get("MODE", "polling")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

    @staticmethod
    def init_logging():
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            level=DefaultConfig.LOG_LEVEL)
        #logging.config.fileConfig('logging.conf')