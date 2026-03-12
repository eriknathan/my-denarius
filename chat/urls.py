from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatView.as_view(), name='index'),
    path('mensagem/', views.ChatMessageView.as_view(), name='message'),
    path('limpar/', views.ChatClearView.as_view(), name='clear'),
]
