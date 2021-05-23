import requests
import json
import telebot
import time
from asgiref.sync import sync_to_async
from .models import Post

#db = Post.objects.all()
api = '1689526123:AAEtzIYtuIjNNVvxNEbSbiKlllzQA0Ia4po'
r = requests.get(f'https://api.telegram.org/bot{api}/getUpdates')
message = 'salamalekum2S'
data = r.json()
print(data)
#chat_id=data['result'][0]['message']['chat']['id']
#request = requests.post(f'https://api.telegram.org/bot{api}/sendMessage?text={message}&chat_id={chat_id}')
#    db = Post.objects.all()


bot = telebot.TeleBot(token = api)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,'salam from ')

def my_scheduled_job():
    
    try:
        bot.polling()
    except Exception:
        time.sleep(10)
        
        

    