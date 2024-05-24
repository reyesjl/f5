from django.db import models
from django.utils import timezone

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