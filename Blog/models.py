from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.db.models import Count
from django.utils import timezone
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver





class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")  # The user receiving the notification
    message = models.CharField(max_length=255)  # Notification message
    is_read = models.BooleanField(default=False)  # Whether the notification is read
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp when the notification is created
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'
    
    class Meta:
        ordering = ['-created_at']



class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255, default='category')
    images = models.ImageField(null=True, blank=True, upload_to="images/")
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
   

    def __str__(self):
        return self.title + ' | '  + str(self.author)
    

    def get_absolute_url(self):
        #return reverse('article-detail', args=(str(self.id))) redirecting my blog post to the article detail 
        return reverse('home') #redirecting my blog back to my home page after posting a blog from thr frontend 
  

    
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pic/', default='default.jpg')
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    snap_url = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    activation_code = models.UUIDField(unique=True, null=True, blank=True)  # Allow NULL temporarily



    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
    
        return reverse('home')
    
    # ✅ Automatically create a profile when a new user is created
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
        


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name= "comments", on_delete=models.CASCADE)    
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)


class Category(models.Model):
    name = models.CharField(max_length=255, default='name')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        #return reverse('article-detail', args=(str(self.id))) redirecting my blog post to the article detail 
        return reverse('home') #redirecting my blog back to my home page after posting a blog from thr frontend 
    




    
