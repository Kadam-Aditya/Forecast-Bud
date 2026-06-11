from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_chatbot, name='ai_chatbot'),
]