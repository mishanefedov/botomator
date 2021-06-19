from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post
import telegram
import telebot
import requests
import time
from asgiref.sync import sync_to_async
import threading
from .bot_handler import BotStarter, BotStopper




#Views
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'app/home.html', context)

class StartBot(threading.Thread, LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Post
    success_url = '/'


    def test_func(self):
        bot = self.get_object()
        print(bot.api)
        bot_data = Post.objects.get(api = bot.api)
        bot_data.running = True
        bot_data.save()
        bot_p = telebot.TeleBot(bot.api)
        BotStarter(bot_p, bot.api, bot_data.message_pairs).start()
        return True
    

class StopBot(threading.Thread, LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Post
    success_url = '/'


    def test_func(self):
        bot = self.get_object()
        print(bot.running)
        to_save = Post.objects.get(api = bot.api)
        to_save.running = False
        to_save.save()
        print(bot.running)
        bot_p = telebot.TeleBot(bot.api)
        BotStopper(bot_p, bot.api).start()
        print('salamalekum')
        return True

class PassView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Post

    def test_func(self):
        bot = self.get_object()
        print(bot.running)
        to_save = Post.objects.get(api = bot.api)
        to_save.running = not bot.running
        to_save.save()
        print(bot.running)
        return True

class PostListView(ListView):
    model = Post
    template_name = 'app/home.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    



class UserPostListView(ListView):
    model = Post
    template_name = 'app/user_posts.html'  
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post
    


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['api', 'name', 'name_id', 'first_message', 'message_pairs']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['api', 'name', 'name_id','first_message', 'message_pairs']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    


def about(request):
    return render(request, 'app/about.html', {'title':'about'})