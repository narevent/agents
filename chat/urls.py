from django.urls import path
from . import views

urlpatterns = [
    path('', views.auto_login, name='auto_login'),
    path('home/', views.home, name='home'),
    path('chat/', views.chat_home, name='chat_home'),
    path('chat/agent/<int:agent_id>/', views.chat_home, name='chat_with_agent'),
    path('chat/conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('agent/create/', views.create_agent, name='create_agent'),
    path('agent/system-prompt/<int:agent_id>/', views.view_system_prompt, name='view_system_prompt'),
    path('api/send/', views.send_message, name='send_message'),
    path('api/new/', views.new_conversation, name='new_conversation'),
    path('api/delete/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
]