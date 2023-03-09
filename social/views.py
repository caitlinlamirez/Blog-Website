from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import ListView
from .models import Post, Profile
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

# Returns the context dictionary for the user profile
def get_profile_context(username):
    # Get the User of the profile
    profile_user = User.objects.get(username=username)
    profile= Profile.objects.get(user=profile_user)
    
    # Get posts by this user and order by descending post date
    user_posts = Post.objects.filter(author=profile_user)
    user_posts = user_posts.order_by('-post_date')
    
    # Get the user's follower and following count
    following_count = Profile.objects.filter(followed_by=profile).count()
    followers_count = Profile.objects.filter(follows=profile).count()
    
    followings = Profile.objects.filter(followed_by=profile)
    followers = Profile.objects.filter(follows=profile)
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': user_posts,
        'following_count': following_count,
        'followers_count': followers_count,
        'followings': followings,
        'followers': followers
    }
    
    return context

# Is the logic behind the POST follow form
def follow_form_logic(request, profile, button):
    # Get current user
    profile_logged_in_user = request.user.profile
    
    # Get form data
    action = request.POST[button]
    # Decide to follow or unfollow
    if action == "unfollow":
        # Unfollow user
        profile_logged_in_user.follows.remove(profile)
    elif action == "follow":
        profile_logged_in_user.follows.add(profile)
        
    profile_logged_in_user.save()

def profile_view(request, username):
    context = get_profile_context(username)
    profile = context.get('profile')
    
    # Post Form logic
    if request.method == "POST":
        follow_form_logic(request, profile, 'follow_button')
        
        # Refreshes the page
        return redirect(request.META['HTTP_REFERER'])
    
    return render(request, 'social/profile_home.html', context )
    
def follow_view(request, username):
    # Get context dictionary 
    context = get_profile_context(username)
    profile = context.get('profile')
    
    # Post Form logic
    if request.method == "POST":
        # If the logged in user clicks the follow button on header
        if 'follow_button' in request.POST:
            follow_form_logic(request, profile, 'follow_button')
            
        # If the logged in user clicks the follow button on a user within the list
        elif 'follow_button2' in request.POST:
            # Get current user
            profile_logged_in_user = request.user.profile
            
            # Get action and target user from the form
            action = request.POST['follow_button2']
            
            # Gets the target_user's profile
            target_username = request.POST['target_user']
            target_user = User.objects.get(username=target_username)
            target_profile = Profile.objects.get(user=target_user)
            
            # Decide to follow or unfollow
            if action == "unfollow":
                # Unfollow user
                profile_logged_in_user.follows.remove(target_profile)
            elif action == "follow":
                profile_logged_in_user.follows.add(target_profile)
                
            profile_logged_in_user.save()
            
            
        # Refreshes the page
        return redirect(request.META['HTTP_REFERER'])
    return render(request, 'social/follow_list.html', context)


@login_required 
def edit_post_view(request, post_id):
    current_post = Post.objects.get(id=post_id)
    # Checks if the post's author matches with the current user
    if (current_post.author == request.user):
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
    else:
        return redirect('dashboard')