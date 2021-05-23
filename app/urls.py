from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, StartBot, StopBot
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name = 'app-home'),
    path('user/<str:username>', UserPostListView.as_view(), name = 'user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name = 'post-delete'),
    path('post/<int:pk>/start', StartBot.as_view(), name = 'bot-start'),
    path('post/<int:pk>/stop', StopBot.as_view(), name = 'bot-stop'),
    path('about/', views.about, name = 'app-about'),
]
