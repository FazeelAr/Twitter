from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=280, blank=True)
    profile_picture = models.ImageField(upload_to='profPic/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    # followers and following logic
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count() 
