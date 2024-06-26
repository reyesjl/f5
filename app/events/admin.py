from django.contrib import admin
from .models import Event, EventRole, Rsvp

# Register your models here.
admin.site.register(Event)
admin.site.register(EventRole)
admin.site.register(Rsvp)
