import asyncio
import json
from django.contrib.auth import get_user_model
from django.db.models import query
import time
import threading
from .models import Post, Thread
import requests



class BotThread(threading.Thread):

    last_message = -1

    def __init__(self, bot):
        self.bot = bot
        self.last_message = self.get_messages()[2]
        threading.Thread.__init__(self)

    
    def run(self):
        print('start thread', self.bot)
        bot = Post.objects.get(id = self.bot.id)
        
        while(bot.running):
            time.sleep(1)
            if self.check_updates():
                print('NEW UPDATE')
                bot = Post.objects.get(id = self.bot.id)
                print(bot.running)
                print('Bot Thread, bot: ', self.bot.id)
                self.handle_messages()
            else:
                print('NO UPDATES OR CHAT EMPTY')    

    def check_updates(self):
        not_empty = self.get_messages()[0] > 0
        if not_empty:
            helper = self.get_messages()[2]
            print("HELPER", helper)
            print("WITH", self.last_message)
            if  helper == self.last_message:
                return False
            else:
                self.last_message = helper
                return True
        return not_empty
        

    def get_messages(self):
        api = self.bot.api
        r = requests.get(f'https://api.telegram.org/bot{api}/getUpdates')
        user_messages = r.json()['result']
        length = len(user_messages)
        last_message = user_messages[length-1]['message']['text']
        chat_id = user_messages[length-1]['message']['chat']['id']
        return length, user_messages, last_message, chat_id

    def handle_messages(self):
        last_message = self.get_messages()[2]
        if last_message in self.bot.message_pairs[0]:
            print("response with ", self.bot.message_pairs[0][last_message])
        else: 
            print("Message not found")
        return True
