from django.urls import path 
from . import views

urlpatterns = [ 
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('create_post', views.create_post, name='create_post'),
    path('logout_user', views.logout_user, name='logout'),
    path('my_profile/<str:username>', views.current_profile_view, name='current_profile')
]
 