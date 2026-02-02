from django import forms
from .models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name', 'category', 'description', 'system_prompt']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent', 'placeholder': 'e.g., Psychology Expert'}),
            'category': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent', 'placeholder': 'e.g., Analyze'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent', 'rows': 3, 'placeholder': 'Brief description of what this agent does...'}),
            'system_prompt': forms.Textarea(attrs={'class': 'w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-mono text-sm', 'rows': 20}),
        }
