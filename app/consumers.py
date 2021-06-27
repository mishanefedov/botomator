import asyncio
import json
from django.contrib.auth import get_user_model
from django.db.models import query
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
import time
import threading
from .models import Post, Thread
import requests
from .bot_thread import BotThread

class Consumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('Connected', event)
        await self.send({
            'type': 'websocket.accept'
        })
        bot = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        print(bot, me)
        
        bot = await self.get_bot(me, bot)

        if(bot.running):
            print(True)            
            await self.start_bot(bot)
            print('bot started')
        else:
            print(False, 'bot stopped')

        await self.send({
            'type':'websocket.send',
            'text':'Salamalekum'
        })


    async def websocket_receive(self, event):
        print('Recieved', event)

    async def websocket_sidconnect(self, event):
        print('Diconnected', event)

    async def start_bot(self, bot):
        bot = BotThread(bot)
        bot.start()
        return True

    
    @database_sync_to_async
    def get_bot(self, user, bot):
        print('Get Bot')
        res = Post.objects.get_bot(user, bot)
        print(res)
        return res

    @database_sync_to_async
    def get_thread(self, user, bot):
        print('GET THREAD')
        res = Thread.objects.get_or_new(user, bot)[0]
        print('RETURN',res)
        return res


