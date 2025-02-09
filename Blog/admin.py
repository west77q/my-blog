from django.contrib import admin
from .models import Post,  Comment, Profile, Category, Like, Notification


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Notification)