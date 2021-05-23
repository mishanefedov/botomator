from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .bot_handler import BotStarter
import telebot
#from collections import OrderedDict
#from dictionaryfield import DictionaryField
#from tablefield.fields import TableField
#from hashid_field import HashidField
#from matrix_field import MatrixField
from jsonfield import JSONField

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
        
