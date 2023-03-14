from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
from datetime import datetime
from django.utils import timezone
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg',upload_to='profile_pics')
    bio = models.TextField(default='Welcome to my profile!', max_length=160)
    follows = models.ManyToManyField("self",
            related_name="followed_by",
            symmetrical=False,
            blank=True) # User does not have to follow anybody
    
    def __str__(self):
        return f'{self.user.username} Profile'
    

# Create Profile when a new user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
post_save.connect(create_profile, sender=User)


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Deletes all of the user's posts if they delete the user
    rating = models.IntegerField(default=0)
    body = models.TextField() 
    post_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    
    @property
    def duration(self):
        if self.post_date:
            time  = timezone.now() 
            if self.post_date.hour == time.hour and self.post_date.day == time.day:
                if time.minute - self.post_date.minute < 0 :
                    return str(time.minute - self.post_date.minute + 60) + " minutes ago"
                if time.minute - self.post_date.minute != 1:
                    return str(time.minute - self.post_date.minute) + " minutes ago"
                else:
                    return str(time.minute - self.post_date.minute) + " minute ago"
                
            elif self.post_date.day == time.day:
                
                if time.hour - self.post_date.hour != 1:
                    return str(time.hour - self.post_date.hour) + " hours ago"
                else:
                    return str(time.hour - self.post_date.hour) + " hour ago"
                
            elif self.post_date.month == time.month:
                
                if time.day - self.post_date.day != 1:
                    return str(time.day - self.post_date.day) + " days ago"
                else:
                    return str(time.day - self.post_date.day) + " day ago"
                
            elif self.post_date.year == time.year:
                
                if time.month - self.post_date.month != 1:
                    return str(time.month - self.post_date.month) + " months ago"
                else:
                    return str(time.month - self.post_date.month) + " month ago"
                
            return self.post_date
            
    
    def __str__(self):
        # On admin page, we can see title and author
        return str(self.author) + " | " + self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=160) 
    comment_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='comments', blank=True)
    
    def __str__(self):
        return "{}'s Comment on '{}' by {}".format(self.commenter.username , self.post.title, self.post.author)
    
    @property
    def duration(self):
        if self.comment_date:
            time  = datetime.now() 
            if self.comment_date.hour == time.hour and self.comment_date.day == time.day:
                if time.minute - self.comment_date.minute != 1:
                    return str(time.minute - self.comment_date.minute) + " minutes ago"
                else:
                    return str(time.minute - self.comment_date.minute) + " minute ago"
                
            elif self.comment_date.day == time.day:
                
                if time.hour - self.comment_date.hour != 1:
                    return str(time.hour - self.comment_date.hour) + " hours ago"
                else:
                    return str(time.hour - self.comment_date.hour) + " hour ago"
                
            elif self.comment_date.month == time.month:
                
                if time.day - self.comment_date.day != 1:
                    return str(time.day - self.comment_date.day) + " days ago"
                else:
                    return str(time.day - self.comment_date.day) + " day ago"
                
            elif self.comment_date.year == time.year:
                
                if time.month - self.comment_date.month != 1:
                    return str(time.month - self.comment_date.month) + " months ago"
                else:
                    return str(time.month - self.comment_date.month) + " month ago"
                
            return self.comment_date