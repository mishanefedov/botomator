import requests
import json
import telebot
import time
from django.db import models

import threading


class BotStarter(threading.Thread):

    def __init__(self, total, api, json):
        self.total = total
        self.api = api
        self.json =json
        threading.Thread.__init__(self)
        
    def get_self(self):
        return self
    
    def run(self):
        #api = self.api
        #r = requests.get(f'https://api.telegram.org/bot{api}/getUpdates')
        #data = r.json()
        #message = 'salam'
        #chat_id=data['result'][0]['message']['chat']['id']
        #requests.post(f'https://api.telegram.org/bot{api}/sendMessage?text={message}&chat_id={chat_id}')
        #data = self.json[0]
        #test_string = 'salamchik'
        #if test_string in data:
        #    print (data[test_string])
        #print(self.json[0]['salamchik'])
        bot = self.total
        @bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
	        bot.reply_to(message, "Howdy, how are you doing?")
        
        def my_scheduled_job():
    
            try:
                bot.polling()
            except Exception as e:
                print(e)
                time.sleep(10)
        
        print(f'The bot {self.api} was successfully started')
        print('Thread finish')




class BotStopper(threading.Thread):
    
    def __init__(self, total, api):
        self.total = total
        self.api = api
        threading.Thread.__init__(self)

    
    def run(self):
        bot = self.total
        def my_scheduled_job():
    
            try:
                bot.stop_polling()
            except Exception:
                time.sleep(10)
                
        print(f'The bot {self.api} was successfully stopped')
        print('Thread finish')