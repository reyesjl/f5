from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_events, name="list-events"),
    path("submit-event/", views.submit_event, name="submit-event"),
]