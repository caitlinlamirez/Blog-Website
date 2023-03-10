from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Post, Profile, Comment
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
    # Orders Posts by Post Date
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
def edit_post_view(request, post_id):
    current_post = Post.objects.get(id=post_id)
    
    # Checks if the post's author matches with the current user
    if (current_post.author == request.user):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                data = Post.objects.get(id=post_id)
                data.author = request.user
                data.title = request.POST['title']
                data.body = request.POST['body']
                data.rating = request.POST['rating']
                data.save()
            return redirect('view_post', post_id)
        else:
            form = PostForm()
        return render(request, 'social/edit_post.html', 
            {
                'post': current_post
            }) 
    else:
        return redirect('dashboard')
    
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
    
    # Get list of followings and followers
    followings = Profile.objects.filter(followed_by=profile)
    followers = Profile.objects.filter(follows=profile)
    
    
    # Places it all in a context dictionary 
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': user_posts,
        'following_count': following_count,
        'followers_count': followers_count,
        'followings': followings,
        'followers': followers
    }
    
    # Return context
    return context


def profile_view(request, username):
    # Get context dictionary 
    context = get_profile_context(username)
    return render(request, 'social/profile_home.html', context )
    
def followings_view(request, username):
    # Get context dictionary 
    context = get_profile_context(username)
    return render(request, 'social/profile_followings.html', context)


def followers_view(request, username):
    # Get context dictionary 
    context = get_profile_context(username)
    return render(request, 'social/profile_followers.html', context)

    
@login_required 
def like_post_view(request, post_id):
    post = Post.objects.get(id=post_id) 
    
    action = request.POST['like_button']
    
    if action == "like":
        post.likes.add(request.user) 
    
    elif action == "unlike":
        post.likes.remove(request.user)
    
    post.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def follow_view(request, user_id):
    # Get target user's profile
    target_user = User.objects.get(id=user_id)
    target_profile = Profile.objects.get(user=target_user)
    
    # Get current user
    profile_logged_in_user = request.user.profile
    
    # Get form data
    action = request.POST['follow_button']
    
    # Decide to follow or unfollow
    if action == "unfollow":
        # Unfollow user
        profile_logged_in_user.follows.remove(target_profile)
    elif action == "follow":
        # Follow user
        profile_logged_in_user.follows.add(target_profile)
        
    # Save 
    profile_logged_in_user.save()
    return redirect(request.META['HTTP_REFERER'])
    

def view_post_view(request, post_id):
    post = Post.objects.get(id=post_id) 
    comments = Comment.objects.filter(post=post)
    comments = comments.order_by('-comment_date')
    
    context = {
        'post': post,
        'comments': comments
    }
    
    return render(request, 'social/view_post.html', context)

@login_required 
def add_comment_view(request, post_id):
    post = Post.objects.get(id=post_id) 
    if request.method == "POST":
            comment = Comment()
            comment.post = post
            comment.commenter = request.user
            comment.body = request.POST['commentBody']
            comment.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required 
def like_comment_view(request, comment_id):
    comment = Comment.objects.get(id=comment_id) 
    
    action = request.POST['comment_like_button']
    
    if action == "like":
        comment.likes.add(request.user) 
    
    elif action == "unlike":
        comment.likes.remove(request.user)
    
    comment.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required 
def delete_post_view(request, post_id):
    post_to_delete = Post.objects.get(id=post_id) 
    
    if request.method == "POST":
        # Delete Post
        post_to_delete.delete()
        return redirect(request.META['HTTP_REFERER'])
    