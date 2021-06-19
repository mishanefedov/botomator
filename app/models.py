from django.db import models, connection
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from django.db import models

from django.conf import settings
from django.db.models import Q

from jsonfield import JSONField

#https://www.youtube.com/watch?v=RVH05S1qab8 30min<


class PostManager(models.Manager):
    
    def get_bot(self, user, bot):
        bot = Post.objects.get(id = bot)
        return bot

class Post(models.Model):
    api = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default = "default name")
    name_id = models.CharField(max_length=100, default = "default name_id")
    first_message = models.CharField(max_length=100, default = "hello my friend")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    running = models.BooleanField(default = False)
    

    message_pairs = JSONField(default=list)
    objects = PostManager()


    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
        


class BotHandler(models.Model):
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, bot): # get_or_create
        bot_id = bot
        bot = Post.objects.get(id=bot)
        #print('SEARCHING FOR THREAD... ')
        #print(Post.objects.only('id').all())
        #print(Post.objects.get(id=bot))
        #Thread.objects.create(first=user, second=bot)
        #print(Thread.objects.all())
    
        print('1...')
        print('2...')
        #Thread.objects.filter(id = 1).delete()
        Thread.objects.filter(id = 3).delete()
        qs = Thread.objects.filter(
            first = user,
            second = bot
        )

        print('QS: ', qs)
        print(connection.queries[-1])
        if qs.count() == 1:
            print('3...')
            return qs.first(), False
        elif qs.count() > 1:
            print('4...')
            return qs.order_by('timestamp').first(), False
        else:
            print('5...')
            new_relation = Thread.objects.create(
                first=user,
                second=bot,
                id = bot_id
            )
            print('...........')
            print(new_relation)
            print(new_relation.id)
            print(new_relation.first)
            print(new_relation.second)
            print('6....')
            new_relation.id = bot_id
            new_relation.save()
            return new_relation, False



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
