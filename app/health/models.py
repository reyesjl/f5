from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.utils.timesince import timesince
from django_ckeditor_5.fields import CKEditor5Field
from members.models import CustomUser

class ClientQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username=username)

    def by_user(self, user):
        return self.filter(user=user)
    
    def by_trainer(self, username):
        return self.filter(trainer__username=username)
    
class Client(models.Model):
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')

    objects = ClientQuerySet.as_manager()

    def __str__(self):
        return self.user.username
    
class HealthProfile(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='health_profile')
	height = models.DecimalField(max_digits=5, decimal_places=2)
	weight = models.DecimalField(max_digits=5, decimal_places=2)
	squat = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	bench = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	chin_up = models.IntegerField(null=True, blank=True)
	deadlift = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	bronco = models.CharField(max_length=8, null=True, blank=True, help_text="Enter duration in HH:MM format")
	broad_jump = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	vertical = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	forty_meter_sprint = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

	def __str__(self):
		return f"Client Profile of {self.user.username}"
    
class PlanQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published")

    def drafts(self):
        return self.filter(status="draft")

    def featured(self):
        return self.filter(featured=True)

    def by_slug(self, slug):
        return self.get(slug=slug)

    def by_visibility(self, visibility):
        return self.filter(status=visibility)

    def by_tag(self, tag):
        return self.filter(tags__icontains=tag)

    def by_type(self, type):
        return self.filter(type=type)


class Plan(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    TYPE_CHOICES = (
        ("strength_and_conditioning", "Strength & Conditioning"),
        ("nutrition", "Nutrition"),
        ("mental", "Mental"),
        ("other", "Other"),
    )

    READING_TIME_CHOICES = (
        (5, "5 mins"),
        (10, "10 mins"),
        (15, "15 mins"),
        (20, "20 mins"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.CharField(max_length=50, blank=True)
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default="strength_and_conditioning"
    )
    featured = models.BooleanField(default=False)
    excerpt = models.TextField(max_length=300, blank=True)
    document = models.FileField(upload_to='health/plans/document/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200, blank=True)
    featured_image = models.ImageField(
        upload_to="health/plans/covers/", blank=True, null=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    objects = PlanQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            if not self.created_at:
                self.created_at = timezone.now()
            date_str = self.created_at.strftime("%Y-%m-%d")
            self.slug = slugify(f"{self.title}-{date_str}")
        super().save(*args, **kwargs)

    def add_view(self):
        self.views += 1
        self.save(update_fields=["views"])

    def __str__(self):
        return self.title

class TrainerSessionRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'), 
        ('accepted', 'Accepted'), 
        ('rejected', 'Rejected')
        )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='session_requests')
    trainer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trainer_sessions')
    requested_date = models.DateField()
    requested_time = models.TimeField()
    additional_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    @property
    def time_since_creation(self):
        delta = timezone.now() - self.created_at
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days}d ago"
        elif hours > 0:
            return f"{hours}h ago"
        else:
            return f"{minutes}m ago"

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} requests {self.trainer.username} for {self.requested_date} at {self.requested_time}"