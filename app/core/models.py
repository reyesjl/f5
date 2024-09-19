from django.db import models

class TourInquiry(models.Model):
    INQUIRY_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    num_people = models.PositiveIntegerField()
    internal_status = models.CharField(
        max_length=10, 
        choices=INQUIRY_STATUS_CHOICES, 
        default='pending'
    )

    def __str__(self):
        return f"Tour Inquiry by {self.name}"
