from django.db import models

class TrainerRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    trainer_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} requested {self.trainer_name} - {self.status}"
    
class Plan(models.Model):
    GOAL_CHOICES = [
        ('strength', 'Strength'),
        ('conditioning', 'Conditioning'),
        ('speed', 'Speed'),
        ('endurance', 'Endurance'),
        ('recovery', 'Recovery'),
    ]

    name = models.CharField(max_length=100)
    trainer_name = models.CharField(max_length=100, blank=True)
    pdf = models.FileField(upload_to='health/fitness_plans/')
    goal = models.CharField(max_length=50, choices=GOAL_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.trainer_name}"
