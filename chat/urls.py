from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversations_list, name='conversations_list'),
    path('<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
]
