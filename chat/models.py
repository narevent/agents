from django.db import models
from django.contrib.auth.models import User

class Agent(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    system_prompt = models.TextField()
    description = models.TextField(blank=True)
    folder_name = models.CharField(max_length=200, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_custom = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.category}: {self.name}"
    
    def get_icon(self):
        """Generate icon based on category"""
        icons = {
            'analyze': '🔍',
            'create': '✨',
            'diagram': '📊',
            'teach': '📚',
            'write': '✍️',
            'code': '💻',
            'data': '📈',
            'design': '🎨',
            'plan': '📋',
            'research': '🔬',
        }
        category_lower = self.category.lower()
        for key, icon in icons.items():
            if key in category_lower:
                return icon
        return '🤖'

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} - {self.agent.name}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=[('user', 'User'), ('assistant', 'Assistant')])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"