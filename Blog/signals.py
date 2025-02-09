from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post, Comment, Notification

# Notify users when a new post is published
@receiver(post_save, sender=Post)
def post_published(sender, instance, created, **kwargs):
    if created:
        # Notify all users except the post creator
        users_to_notify = User.objects.exclude(id=instance.author.id)
        for user in users_to_notify:
            message = f"A new post titled '{instance.title}' has been published by {instance.author}."
            post_url = reverse('article-detail', args=[instance.id])
            # Create a notification
            Notification.objects.create(user=user, message=message, url=post_url)

@receiver(post_save, sender=Comment)
def comment_added(sender, instance, created, **kwargs):
    if created:
        post = instance.post  # Get the post related to the comment
        author = post.author  # The author of the post being commented on
        
        # Check if the name of the commenter is the same as the post author
        if instance.name != author.username:  # Assuming 'name' is the commenter's username
            message = f"{instance.name} commented on your post: {post.title}"
            
            # Correct: Use post.pk to get the post ID, not comment ID
            post_url = reverse('article-detail', args=[post.pk])
            
            # Create a notification for the post author
            Notification.objects.create(user=author, message=message, url=post_url)
            print(f"A new comment was added to the post: '{post.title}' by {instance.name}")  # Debugging log
        else:
            print(f"{instance.name} commented on their own post. No notification sent.")

