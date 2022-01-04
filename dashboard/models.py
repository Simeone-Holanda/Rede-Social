from django.db import models
from django.utils import timezone
from accounts.models import User

class Post(models.Model):
    text = models.TextField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='posts')

class Comment(models.Model):
    text = models.TextField(max_length=150, null=False)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=False) #, related_name='comments'

class Like(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

class Notification(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    message = models.TextField(max_length=100, null=False)
    status = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='notifications')

class Follower(models.Model):
    follow_date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_profile')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='followers')

    