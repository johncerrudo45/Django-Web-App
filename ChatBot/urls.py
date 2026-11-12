from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name = 'chatbot'),                  # path for accessing website
    path('send/', views.chat, name = 'chat')                    # path for sending ai chatbot response
]