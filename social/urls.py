from django.urls import path 
from . import views

urlpatterns = [ 
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('create_post', views.create_post, name='create_post'),
    path('logout_user', views.logout_user, name='logout'),
    path('profile/<str:username>', views.profile_view, name='user_profile'),
    path('profile/<str:username>/follow-list', views.follow_view, name='follow_list'),
    path('edit_post/<int:post_id>', views.edit_post_view, name='edit_post')
]
 