from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from .models import Post
from .forms import PostForm

@method_decorator(login_required, name='dispatch')
class DashboardView(ListView):
    model = Post 
    template_name = 'social/dashboard.html'
    ordering = ['-post_date']
    
@method_decorator(login_required, name='dispatch')
class CreatePostView(CreateView):
    model = Post 
    form_class = PostForm
    template_name = 'social/create_post.html'
    # fields = '__all__'