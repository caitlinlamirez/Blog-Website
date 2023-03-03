from django.urls import path 
from . import views
from .views import DashboardView

urlpatterns = [ 
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('create_post', views.create_post, name='create_post'),
]