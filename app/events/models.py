import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

class EventQuerySet(models.QuerySet):
    def by_slug(self, slug):
        return self.get(slug=slug)
    
    def by_id(self, event_id):
        return self.get(pk=event_id)

    def by_type(self, event_type):
        return self.filter(event_type=event_type)
    
    def filter_by_event_type(self, event_type):
        if event_type:
            return self.filter(event_type=event_type)
        return self
    
    def past(self):
        now = timezone.now()
        return self.filter(start_date__lte=now)
    
    def upcoming(self):
        now = timezone.now()
        return self.filter(start_date__gte=now)
    
    def featured(self):
        return self.filter(featured=True).order_by('start_date')

class Event(models.Model):
    EVENT_TYPES = (
        ('camp', 'Camp'),
        ('game', 'Game'),
        ('training', 'Training'),
        ('clinic', 'Clinic'),
        ('tournament', 'Tournament'),
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
    payment_required = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=True)

    objects = EventQuerySet.as_manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            date_str = self.start_date.strftime("%Y-%m-%d")
            self.slug = slugify(f"{self.name}-{date_str}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class EventRole(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event, related_name='roles', on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.name} for {self.event.name}'

class RsvpQuerySet(models.QuerySet):
    def by_slug(self, slug):
        return self.get(slug=slug)
    
    def by_token(self, token):
        return self.get(token=token)
    
    def email_exists_for(self, event, email):
        return self.filter(event=event, email__iexact=email).exists()
    
    def phone_exists_for(self, event, phone_number):
        return self.filter(event=event, phone_number__iexact=phone_number).exists()
    
    def by_event(self, event):
        return self.filter(event=event)
    
    def by_event_and_slug(self, event, rsvp_slug):
        return self.get(event=event, slug=rsvp_slug)
    
    def filter_by_paid_status(self, paid_status):
        if paid_status is not None:
            return self.filter(has_paid=paid_status)
        return self

class Rsvp(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    role = models.ForeignKey(EventRole, related_name='rsvps', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    has_paid = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=True)

    objects = RsvpQuerySet.as_manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            if not self.token:
                self.token = uuid.uuid4()
            self.slug = slugify(f"{self.token}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name} - {self.event.name}'

    def payment_status_and_cost(self):
        if not self.event.payment_required:
            return {'status': 'No Payment Required', 'cost': 0}

        # All pay 'cost'
        if self.event.event_type == 'game' :
            cost = self.event.cost
        elif self.event.event_type == 'camp':
            # Player pays 'cost'
            # Coach pays 'cost_secondary'
            cost = self.event.cost if self.role == 'player' else self.event.cost_secondary
        else:
            cost = self.event.cost

        if not self.has_paid:
            return {'status': 'Not Paid', 'cost': cost}
        else:
            return {'status': 'Paid', 'cost': 0}