from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Post
from .forms import PostForm
from django.contrib.auth import logout 
from django.contrib import messages 
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have successfuly logged out")
    return redirect('login')

@login_required
def dashboard_view(request):
    posts = Post.objects.all().order_by('-post_date')
    context = {
        'posts': posts
    }
    return render(request, 'social/dashboard.html', context)
    
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            data = Post()
            data.author = request.user
            data.title = form.cleaned_data['title']
            data.body = form.cleaned_data['body']
            data.rating = form.cleaned_data['rating']
            data.save()
            return redirect('dashboard')
    else:
        form = PostForm()
    return render(request, 'social/create_post.html', {}) 

@login_required
def current_profile_view(request, username):
    # If the username matches the current user logged in
    if username == request.user.username:
        user_posts = Post.objects.filter(author=request.user)
        user_posts = user_posts.order_by('-post_date')
        return render(request, 'social/current_profile.html', 
        {
            'posts': user_posts
        })
    
    # Otherwise redirect to the dashboard
    else:
        return redirect('dashboard')
                
@login_required 
def edit_post_view(request, post_id):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            data = Post.objects.get(id=post_id)
            data.author = request.user
            data.title = form.cleaned_data['title']
            data.body = form.cleaned_data['body']
            data.rating = form.cleaned_data['rating']
            data.post_date = datetime.now()
            data.save()
            return redirect('dashboard')
    else:
        post = Post.objects.get(id=post_id)
        form = PostForm()
        return render(request, 'social/edit_post.html', {
            'post': post
        }) 