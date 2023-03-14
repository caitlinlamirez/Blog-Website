from django.urls import path 
from . import views

urlpatterns = [ 
    path('', views.landing_view, name='landing'),
    path('login', views.login_user, name='login'),
    path('register', views.register_user, name='register'),
]