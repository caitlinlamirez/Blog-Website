from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages 
from .forms import RegisterUserForm


def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            # Takes input we got from the html file and store them
            username = request.POST['username']
            password = request.POST['password']
            
            # Sees if they are correct
            user = authenticate(request, username=username, password=password)
            
            # Valid login
            if user is not None:
                login(request, user)
                # Redirect to login url
                return redirect('dashboard')
                
            # Invalid login
            else:
                messages.error(request, "Invalid Username/Password. Please try again.")
                # Return an 'invalid login' error message.
                return redirect('login')
        else:
            return render(request, 'landing/login.html', {}) 
    else:
        return redirect('dashboard')
    
    
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
            return redirect('dashboard')
        else:
            messages.error(request, form.errors)
            return redirect('register')
    else:
        # Pass in the form
        form = RegisterUserForm() 
    return render(request, 'landing/register.html', {
        'form': form,
    })
    