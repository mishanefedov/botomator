from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .bot_handler import BotStarter
import telebot

from django.db import models

from django.conf import settings
from django.db.models import Q

from users.models import Profile

from jsonfield import JSONField

#https://www.youtube.com/watch?v=RVH05S1qab8 30min<

class Post(models.Model):
    api = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default = "default name")
    name_id = models.CharField(max_length=100, default = "default name_id")
    first_message = models.CharField(max_length=100, default = "hello my friend")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    running = models.BooleanField(default = False)
    
    message_pairs = JSONField(default=list)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
        


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, bot): # get_or_create
        print('SEARCHING FOR THREAD... ')
        username = user.username
        if username == bot:
            return None
        print('1...')
        qlookup1 = Q(first__username=username) & Q(second__username=bot)
        qlookup2 = Q(first__username=bot) & Q(second__username=username)
        print('2...')
        print('SELF QUERYSET', self.get_queryset().count())

        qs = self.get_queryset().distinct()
        print(qs)
        if qs.count() == 1:
            print('3...')
            return qs.first(), False
        elif qs.count() > 1:
            print('4...')
            return qs.order_by('timestamp').first(), False
        else:
            print('5...')
            user2 = Post.objects.get(id=bot)
            print(user2)
            print('555...')
            print(user2)
            if user != user2:
                obj = self.model(
                        first=user, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False



class Thread(models.Model):
    first        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
    second       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated      = models.DateTimeField(auto_now=True)
    timestamp    = models.DateTimeField(auto_now_add=True)
    
    objects      = ThreadManager()

    def __str__(self):
        return F'{self.first}  {self.second}'

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False
