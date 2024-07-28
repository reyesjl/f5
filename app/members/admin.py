from django.contrib import admin
from .models import CustomUser, UserProfile, SupportTicket, Avatar

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_trainer', 'bio')
    search_fields = ('username', 'bio')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'avatar')
    search_fields = ('user__username',)

admin.site.register(SupportTicket)
admin.site.register(Avatar)