from django.db import models
from members import CustomUser

class Achievement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/')
    points = models.IntegerField()

    def __str__(self):
        return self.title

class UserAchievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achieved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.achievement.title}"