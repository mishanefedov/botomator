import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Post, Thread

class Consumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Connected', event)
        await self.send({
            'type': 'websocket.accept'
        })
        bot = self.scope['url_route']['kwargs']['username']
        print('BOT/////////',bot)
        me = self.scope['user']
        print(bot, me)
        thread_obj = await self.get_thread(me, bot)
        print(thread_obj)
        #await asyncio.sleep(10)
        await self.send({
            'type':'websocket.send',
            'text':'Salamalekum'
        })

    async def websocket_receive(self, event):
        print('Recieved', event)

    async def websocket_sidconnect(self, event):
        print('Diconnected', event)

    @database_sync_to_async
    def get_thread(self, user, bot):
        res = Thread.objects.get_or_new(user, bot)[0]
        print('RETURN',res)
        return res