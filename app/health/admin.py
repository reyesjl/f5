from django.contrib import admin
from .models import Plan, Client, HealthProfile, TrainerSessionRequest

admin.site.register(Plan)
admin.site.register(Client)
admin.site.register(HealthProfile)
admin.site.register(TrainerSessionRequest)