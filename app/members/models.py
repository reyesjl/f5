from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    def reset_health_profile(self):
        health_profile, created = HealthProfile.objects.get_or_create(user=self)
        health_profile.height = 0.00
        health_profile.weight = 0.00
        health_profile.save()

    def erase_profiles(self):
        HealthProfile.objects.filter(user=self).delete()

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

class HealthProfile(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='health_profile')
	height = models.DecimalField(max_digits=5, decimal_places=2)
	weight = models.DecimalField(max_digits=5, decimal_places=2)
	squat = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	bench = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	chin_up = models.IntegerField(null=True, blank=True)
	deadlift = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	bronco = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	broad_jump = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	vertical = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	forty_meter_sprint = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

	def __str__(self):
		return f"Health Profile of {self.user.username}"


class SupportTicket(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject