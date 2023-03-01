from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm


def login_user(request):
    if request.method == "POST":
        # Takes input we got from the html file and store them
        username = request.POST['username']
        password = request.POST['password']
        
        # Sees if they are correct
        user = authenticate(request, username=username, password=password)
        
        # Valid login
        if user is not None:
            messages.success(request, "Success!")
            login(request, user)
            # Redirect to login url
            return redirect('dashboard')
            
        # Invalid login
        else:
            messages.success(request, "There was an error logging in!")
            # Return an 'invalid login' error message.
            return redirect('login')
    else:
        return render(request, 'landing/login.html', {}) 
    
    
def register_user(request):
    # If they did fill out the form
    if request.method == "POST": 
        # If user fills out form, we pass that into a RegisterUserForm
        form = RegisterUserForm(request.POST)  
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            # Logs them in
            user = authenticate(username=username, password=password)
            login (request, user)
            messages.success(request, "Registration and Login successful!")
            return redirect('login')
    else:
        # Pass in the form
        form = RegisterUserForm() 
    return render(request, 'landing/register.html', {
        'form': form,
    })