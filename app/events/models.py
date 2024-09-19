from django.db import models
from django.utils.text import slugify

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            date_str = self.start_date.strftime("%Y-%m-%d")
            self.slug = slugify(f"{self.name}-{date_str}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class EventSubmission(models.Model):
    SUBMISSION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    event_name = models.CharField(max_length=255)
    event_description = models.TextField()
    event_date = models.DateField()
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    internal_status = models.CharField(
        max_length=20, 
        choices=SUBMISSION_STATUS_CHOICES, 
        default='pending'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.name} for {self.event_name}"