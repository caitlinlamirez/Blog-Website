from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
from datetime import datetime
from django.utils import timezone
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg',upload_to='profile_pics')
    header = models.ImageField(default='default_header.png', upload_to='header_pics')
    bio = models.TextField(default='Welcome to my profile!')
    
    
    def __str__(self):
        return f'{self.user.username} Profile'
    

# Create Profile when a new user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
post_save.connect(create_profile, sender=User)


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Deletes all of the user's posts if they delete the user
    rating = models.IntegerField(default=0)
    body = models.TextField() 
    post_date = models.DateTimeField(default=timezone.now)
    
    @property
    def duration(self):
        if self.post_date:
            time  = datetime.now() 
            if self.post_date.hour == time.hour:
                
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
