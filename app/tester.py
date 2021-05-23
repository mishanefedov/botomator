import requests
import json
import telebot
import time
from django.db import models

import threading



bot = telebot.TeleBot(token = '1689526123:AAEtzIYtuIjNNVvxNEbSbiKlllzQA0Ia4po')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
        
def my_scheduled_job():
    
    try:
        bot.polling()
    except Exception as e:
        print(e)
        time.sleep(10)