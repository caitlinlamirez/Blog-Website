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
    
    # If user wants to delete a post
    if request.method == "POST":
        if "delete_button" in request.POST:
            # Get Post ID 
            post_id = request.POST['delete_button']
            
            # Get Post object using the Post ID
            post_to_delete = Post.objects.get(id=post_id)
            
            # Delete Post
            post_to_delete.delete()
            return redirect(request.META['HTTP_REFERER'])
    else:
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
        # Follow user
        profile_logged_in_user.follows.add(profile)
        
    # Save 
    profile_logged_in_user.save()

def profile_view(request, username):
    context = get_profile_context(username)
    profile = context.get('profile')
    
    # If user clicks on the follow/unfollow button
    if request.method == "POST":
        if 'follow_button' in request.POST:
            # Performs the action on the user on that profile
            follow_form_logic(request, profile, 'follow_button')
            
            # Refreshes the page
            return redirect(request.META['HTTP_REFERER'])
        elif "delete_button" in request.POST:
            # Get Post ID 
            post_id = request.POST['delete_button']
            
            # Get Post object using the Post ID
            post_to_delete = Post.objects.get(id=post_id)
            
            # Delete Post
            post_to_delete.delete()
            return redirect(request.META['HTTP_REFERER'])
    
    return render(request, 'social/profile_home.html', context )
    
def followings_view(request, username):
    # Get context dictionary 
    context = get_profile_context(username)
    profile = context.get('profile')
    
    # If user clicks on the follow/unfollow button
    if request.method == "POST":
        # If the logged in user clicks the follow button on header
        if 'follow_button' in request.POST:
            # Performs the action on the user on that profile
            follow_form_logic(request, profile, 'follow_button')
            
        # If the logged in user clicks the follow button on a user within the list
        elif 'follow_button2' in request.POST:
            # Gets the target_user's profile
            target_username = request.POST['target_user']
            target_user = User.objects.get(username=target_username)
            target_profile = Profile.objects.get(user=target_user)
            
            # Performs the action on the target user
            follow_form_logic(request, target_profile, 'follow_button2')
            
            
        # Refreshes the page
        return redirect(request.META['HTTP_REFERER'])
    return render(request, 'social/profile_followings.html', context)


def followers_view(request, username):
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
    return render(request, 'social/profile_followers.html', context)

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