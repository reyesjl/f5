from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
   pass

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)

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

class PlayerProfile(models.Model):
   user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   position = models.CharField(max_length=50)
   club = models.CharField(max_length=100)
   tries_scored = models.IntegerField(default=0)
   tackles_made = models.IntegerField(default=0)
   minutes_played = models.IntegerField(default=0)

class HealthProfile(models.Model):
   user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   height = models.DecimalField(max_digits=5, decimal_places=2)
   weight = models.DecimalField(max_digits=5, decimal_places=2)
