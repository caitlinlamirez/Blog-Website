from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm



class PostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = [ 'title', 'body', 'rating']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = [ 'body' ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = [ 'bio', 'image' ]
        
class FullNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name' ]
        
class FullNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name' ]
        
class UserAccountForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = [ 'username', 'first_name', 'last_name', 'email' ]
        
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.PasswordInput() 
    new_password1 = forms.PasswordInput() 
    new_password2 = forms.PasswordInput() 
    class Meta:
        model = User 
        fields = ('old_password', 'new_password1', 'new_password2')

