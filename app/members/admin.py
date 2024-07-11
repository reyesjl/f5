from django.contrib import admin
from .models import CustomUser, UserProfile, PlayerProfile, HealthProfile, SupportTicket

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(PlayerProfile)
admin.site.register(HealthProfile)
admin.site.register(SupportTicket)