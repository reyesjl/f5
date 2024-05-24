import uuid
from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

class EventQuerySet(models.QuerySet):
    def by_event_id(self, event_id):
        return self.get(pk=event_id)

    def by_event_type(self, event_type):
        return self.filter(event_type=event_type)
    
    def past_events(self):
        now = timezone.now()
        return self.filter(start_date__lte=now)
    
    def upcoming_events(self):
        now = timezone.now()
        return self.filter(start_date__gte=now)
    
    def featured_events(self):
        return self.filter(featured=True)

class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)
    
    def by_event_id(self, event_id):
        return self.get_queryset().by_event_id(event_id)

    def by_event_type(self, event_type):
        return self.get_queryset().by_event_type(event_type)
    
    def past_events(self):
        return self.get_queryset().past_events()
    
    def upcoming_events(self):
        return self.get_queryset().upcoming_events()
    
    def featured_events(self):
        return self.get_queryset().featured_events()

class Event(models.Model):
    EVENT_TYPES = (
        ('camp', 'Camp'),
        ('game', 'Game'),
        ('training', 'Training'),
        ('clinic', 'Clinic'),
        ('combine', 'Combine'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    detailed_description = CKEditor5Field('Text', config_name='extends', default=None, blank=True, null=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    featured = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    registration_required = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    objects = EventManager()

    def __str__(self):
        return self.name
    
class RsvpQuerySet(models.QuerySet):
    def by_token(self, token):
        return self.get(token=token)
    
    def email_exists_for_event(self, event, email):
        return self.filter(event=event, email__iexact=email).exists()
    
    def phone_exists_for_event(self, event, phone_number):
        return self.filter(event=event, phone_number__iexact=phone_number).exists()

class RsvpManager(models.Manager):
    def get_queryset(self):
        return RsvpQuerySet(self.model, using=self._db)
    
    def by_token(self, token):
        return self.get_queryset().by_token(token)
    
    def email_exists_for_event(self, event, email):
        return self.get_queryset().email_exists_for_event(event, email)

    def phone_exists_for_event(self, event, phone_number):
        return self.get_queryset().phone_exists_for_event(event, phone_number)

class Rsvp(models.Model):
    ROLE_CHOICES = (
        ('player', 'Player'),
        ('coach', 'Coach'),
        ('spectator', 'Spectator'),
    )
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    has_paid = models.BooleanField(default=False)

    objects = RsvpManager()
    
    def __str__(self):
        return f'{self.name} - {self.event.name}'

    class Meta:
        unique_together = ('event', 'email')