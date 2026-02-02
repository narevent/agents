from django.contrib import admin
from .models import Agent, Conversation, Message

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'folder_name', 'is_custom', 'created_at']
    list_filter = ['category', 'is_custom']
    search_fields = ['name', 'description']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'agent', 'created_at', 'updated_at']
    list_filter = ['agent', 'created_at']
    search_fields = ['title']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'created_at']
    list_filter = ['role', 'created_at']