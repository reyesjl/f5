from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("core.urls")),
    path("events/", include("events.urls")),
    path("clubs/", include("clubs.urls")),
    path("admin/", admin.site.urls),
]
