from django.contrib import admin
from .models import CustomUser, UserProfile, SupportTicket, Avatar

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(SupportTicket)
admin.site.register(Avatar)