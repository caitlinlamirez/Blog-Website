from django.urls import path 
from . import views

urlpatterns = [ 
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('create_post', views.create_post, name='create_post'),
    path('logout_user', views.logout_user, name='logout'),
    path('profile/<str:username>', views.profile_view, name='user_profile'),
    path('profile/<str:username>/followings-list', views.followings_view, name='followings_list'),
    path('profile/<str:username>/followers-list', views.followers_view, name='followers_list'),
    path('edit_post/<int:post_id>', views.edit_post_view, name='edit_post'),
    path('like/<int:post_id>', views.like_post_view , name='like_post'),
    path('post/<int:post_id>', views.view_post_view , name='view_post'),
    path('post/<int:post_id>/comment', views.add_comment_view, name='add_comment'),
    path('like/comment/<int:comment_id>', views.like_comment_view, name='like_comment'),
    path('follow/user/<int:user_id>', views.follow_view, name='follow_user'),
    path('post/<int:post_id>/delete', views.delete_post_view, name='delete_post'),
    path('profile/edit_profile/<int:profile_id>', views.edit_profile_view, name='edit_profile'),
    path('account/settings', views.edit_account_view, name='edit_account'),
    path('account/delete', views.delete_account_view, name='delete_account'),
    path('account/reset_password', views.reset_password_view, name='reset_password'),
]
 