from django.contrib import admin
from .models import Comment, Post, Notification, Like, Follower

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Follower)
