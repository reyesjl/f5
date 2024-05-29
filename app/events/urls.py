from django.urls import path

from . import views

urlpatterns = [
    # events
    path("", views.event_list, name="event-list"),
    path("create/", views.event_create, name="event-create"),
    path("<slug:slug>/", views.event_detail, name="event-detail"),
    path("<slug:slug>/update/", views.event_update, name="event-update"),
    path("<slug:slug>/delete/", views.event_delete, name="event-delete"),

    # rsvps
    path("<slug:event_slug>/rsvps/", views.rsvp_list, name="rsvp-list"),
    path("<slug:event_slug>/rsvps/create/", views.rsvp_create, name="rsvp-create"),
    path("<slug:event_slug>/rsvps/<slug:rsvp_slug>/", views.rsvp_detail, name="rsvp-detail"),
    path("<slug:event_slug>/rsvps/<slug:rsvp_slug>/update/", views.rsvp_update, name="rsvp-update"),
    #path("<slug:event_slug>/rsvps/<slug:rsvp_slug>/delete/", views.rsvp_delete, name="rsvp-delete"),
]