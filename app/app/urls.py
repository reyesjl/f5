from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("events/", include("events.urls")),
    path("admin/", admin.site.urls),
]
