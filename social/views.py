from turtle import update
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Post, Profile, Comment
from .forms import PostForm, CommentForm, ProfileForm, FullNameForm, UserAccountForm, PasswordChangingForm
from django.contrib.auth import logout, update_session_auth_hash
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
    # If users wants to sort the posts
    if request.method == "POST":
        sort_by = request.POST.get('sortPosts')
        print(sort_by)
        if sort_by == "newest":
            posts = Post.objects.all().order_by('-post_date')
        elif sort_by == "oldest":
            posts = Post.objects.all().order_by('post_date')
        elif sort_by == "highest_rating":
            posts = Post.objects.all().order_by('-rating')
        elif sort_by == "lowest_rating":
            posts = Post.objects.all().order_by('rating')
        context = {
            'posts': posts,
            'selected_sort': sort_by
        }
        return render(request, 'social/dashboard.html', context)
        
    else:
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
            form = PostForm(request.POST or None, instance = current_post)
            if form.is_valid():
                form.save()
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
def add_comment_view(request, post_id):
    post = Post.objects.get(id=post_id) 
    if request.method == "POST":
        form  = CommentForm(request.POST)
        if form.is_valid():
            print("form valid")
            comment = Comment()
            comment.post = post
            comment.commenter = request.user
            comment.body = form.cleaned_data['body']
            comment.save()
            return redirect('view_post', post_id)
    else:
        form = CommentForm()
    return redirect('view_post', post_id)

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
        post_to_delete.delete()
        return redirect(request.META['HTTP_REFERER'])
    
@login_required
def edit_profile_view(request, profile_id):
    user = request.user
    profile = Profile.objects.get(id=profile_id) 
    if request.method == "POST":
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance = profile)
        fullname_form = FullNameForm(request.POST or None, instance = user)
        if profile_form.is_valid() and fullname_form.is_valid():
            profile_form.save()
            fullname_form.save()
        return redirect(request.META['HTTP_REFERER']) 
    else:
        profile_form = ProfileForm()
        fullname_form = FullNameForm()
    return redirect(request.META['HTTP_REFERER']) 

@login_required 
def edit_account_view(request):
    user = request.user
    if request.method == "POST":
        form = UserAccountForm(request.POST or None, instance=user) 
        if form.is_valid():
            form.save()
            messages.success(request, "Account was updated successfully!")
        return redirect(request.META['HTTP_REFERER']) 
    else:
        form = UserAccountForm()
    return render(request, 'social/edit_account.html')

@login_required
def delete_account_view(request):
    user = request.user 
    if request.method == "POST":
        user.delete() 
        messages.success(request, "Account was deleted successfully")
        return redirect('login')
    return render(request, 'social/edit_account.html')

@login_required 
def reset_password_view(request):
    if request.method == "POST":
        form = PasswordChangingForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, "Your password was successfully reset")
            return redirect('edit_account')
        else:
            for error in form.errors:
                print(form.errors[error])
                messages.error(request, form.errors[error])
            return redirect(request.META['HTTP_REFERER']) 
    else:
        form = PasswordChangingForm(user=request.user)
    return render(request, 'social/reset_password.html')
            
def search_view(request):
    # Get search query
    query = request.GET.get('query')
    
    # Search posts by title and user
    posts_by_title = Post.objects.filter(title__contains = query)
    posts_by_user = Post.objects.filter(author__username__contains = query)

    # Combine query results
    post_results = posts_by_title | posts_by_user

    # Search for profiles
    profile_results = Profile.objects.filter(user__username__contains = query)

    # Context dictionary 
    context = {
        'query': query,
        'posts': post_results,
        'profiles': profile_results
        
    }
    return render(request, 'social/search.html', context)
    
@login_required 
def friends_view(request):
    logged_in_user = request.user
    # If users wants to sort the posts
    if request.method == "POST":

        sort_by = request.POST.get('sortPosts')
        
        # Get logged in user's posts and their followed users' posts
        logged_in_user_posts = Post.objects.filter(author = logged_in_user)
        followings_posts = Post.objects.filter(author__profile__in = logged_in_user.profile.follows.all())

        posts = logged_in_user_posts | followings_posts

        if sort_by == "newest":
            posts = posts.order_by('-post_date')
        elif sort_by == "oldest":
            posts = posts.order_by('post_date')
        elif sort_by == "highest_rating":
            posts = posts.order_by('-rating')
        elif sort_by == "lowest_rating":
            posts = posts.order_by('rating')
        context = {
            'posts': posts,
            'selected_sort': sort_by,
        }
        return render(request, 'social/friends_posts.html', context)
        
    else:
        # Get logged in user's posts and their followed users' posts
        logged_in_user_posts = Post.objects.filter(author = logged_in_user)
        followings_posts = Post.objects.filter(author__profile__in = logged_in_user.profile.follows.all())

        posts = logged_in_user_posts | followings_posts
        posts = posts.order_by('-post_date')
        context = {
            'posts': posts
        }
        return render(request, 'social/friends_posts.html', context)
            
            