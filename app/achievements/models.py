from django.db import models
from members import CustomUser

class Achievement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/')
    points = models.IntegerField()

    def __str__(self):
        return self.title

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

class UserAchievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achieved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.achievement.title}"