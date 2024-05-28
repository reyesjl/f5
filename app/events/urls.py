from django.urls import path

from . import views

urlpatterns = [
    path("", views.event_list, name="event-list"),
    path("filter/type/<str:event_type>/", views.events_by_type, name="events-by-type"),
    path("create/", views.event_create, name="event-create"),
    path("<slug:slug>/", views.event_detail, name="event-detail"),
    path("<slug:slug>/update/", views.event_update, name="event-update"),
    path("<slug:slug>/delete/", views.event_delete, name="event-delete"),
]