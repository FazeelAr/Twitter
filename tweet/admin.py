from django.contrib import admin
from .models import Tweet, Comment, Like

admin.site.register(Tweet)
admin.site.register(Like)
admin.site.register(Comment)
