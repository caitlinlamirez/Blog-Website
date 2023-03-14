from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 

# Inherits from UserCreation Form
class RegisterUserForm(UserCreationForm):
    # Create the additional fields
    # Widget turns field into bootstrapped fields
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    
    class Meta:
        model = User 
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        