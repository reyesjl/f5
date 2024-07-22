from django.contrib import admin
from .models import Plan, Client, HealthProfile, Exercise, Movement


admin.site.register(Plan)
admin.site.register(Client)
admin.site.register(HealthProfile)
admin.site.register(Exercise)
admin.site.register(Movement)