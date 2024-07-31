from django.db import models
from django.contrib.auth.models import AbstractUser
from .services import AvatarService
from PIL import Image

class CustomUser(AbstractUser):
    is_trainer = models.BooleanField(
        default=False,
        verbose_name='Trainer status',
        help_text='Designates whether this user is a trainer.'
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='profiles/avatars/', null=True, blank=True, default='members/images/default_avatar.jpg')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            avatar_path = self.avatar.path
            img = Image.open(avatar_path)

            # Ensure the image is a square
            width, height = img.size
            if width != height:
                new_size = min(width, height)
                left = (width - new_size) / 2
                top = (height - new_size) / 2
                right = (width + new_size) / 2
                bottom = (height + new_size) / 2
                img = img.crop((left, top, right, bottom))

            # Resize the image to 400x400 pixels
            img = img.resize((400, 400), Image.ANTIALIAS)
            img.save(avatar_path)

    def __str__(self):
        return self.username

class Avatar(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profiles/avatars/')

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def add_xp(self, points):
        self.xp += points
        self.check_level_up()
        self.save()

    def check_level_up(self):
    	# Simple example: increase level for every 1000 XP
        while self.xp >= self.level * 1000:
            self.level += 1

class SupportTicket(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject