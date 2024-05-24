from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('type/<str:event_type>/', views.events_by_type, name='events_by_type'),
    path('details/<int:event_id>/', views.event_details, name='event_details'),
]