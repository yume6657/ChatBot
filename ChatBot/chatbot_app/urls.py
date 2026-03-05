from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/', views.chat_view, name='chat'),
    path('api/conversations/', views.get_conversations, name='get_conversations'),
    path('api/conversations/<int:conversation_id>/messages/', views.get_messages, name='get_messages'),
    path('api/send_message/', views.send_message, name='send_message'),
    path('api/conversations/create/', views.create_conversation, name='create_conversation'),
    path('api/conversations/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('api/user_stats/', views.get_user_stats, name='get_user_stats'),
]