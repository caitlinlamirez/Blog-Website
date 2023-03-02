from typing import Text
from django import forms
from .models import Post 

class PostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = [ 'title', 'body']
        labels = {
            'title': 'Post Title',
            'body': 'Your Post'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }