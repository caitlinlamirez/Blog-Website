from django.urls import path 
from . import views
from .views import DashboardView, CreatePostView

urlpatterns = [ 
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('create_post', CreatePostView.as_view(), name='create_post'),
]