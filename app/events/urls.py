from django.urls import path

from . import views

urlpatterns = [
    # events
    path("", views.event_list, name="event-list"),
    path("filter/type/<str:event_type>/", views.events_by_type, name="events-by-type"),
    path("create/", views.event_create, name="event-create"),
    path("<slug:slug>/", views.event_detail, name="event-detail"),
    path("<slug:slug>/update/", views.event_update, name="event-update"),
    path("<slug:slug>/delete/", views.event_delete, name="event-delete"),

    # rsvps
    #path("rsvp/", views.rsvp_list, name="rsvp-list"),
    path("rsvps/filter/<slug:event_slug>/", views.rsvp_by_event, name="rsvp-by-event"),
    path("rsvps/create/<slug:event_slug>", views.rsvp_create, name="rsvp-create"),
    path("rsvps/<slug:slug>/", views.rsvp_detail, name="rsvp-detail"),
]