from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("core.urls")),
    path("events/", include("events.urls")),
    path("clubs/", include("clubs.urls")),
    path("health/", include("health.urls")),
    path("blog/", include("blog.urls")),
    path("members/", include("members.urls")),
    path("members/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
