from django.urls import path

from . import views

urlpatterns = [
    #path("", views.event_list, name="event-list"),
    #path("create/", views.event_create, name="event-create"),
    #path("<slug:slug>/", views.event_detail, name="event-detail"),
    #path("<slug:slug>/update/", views.event_update, name="event-update"),
    #path("<slug:slug>/delete/", views.event_delete, name="event-delete"),

    # events 2.0
    path("", views.list_events, name="list-events"),

    # event roles
    path("<slug:event_slug>/roles/", views.role_list, name="role-list"),
    path("<slug:event_slug>/roles/create/", views.role_create, name="role-create"),
    path("<slug:event_slug>/roles/<int:role_id>/delete/", views.role_delete, name="role-delete"),

    # rsvps
    path("<slug:event_slug>/rsvps/", views.rsvp_list, name="rsvp-list"),
    path("<slug:event_slug>/rsvps/create/", views.rsvp_create, name="rsvp-create-no-role"),
    path("<slug:event_slug>/rsvps/create/<int:role_id>/", views.rsvp_create, name="rsvp-create"),
    path("<slug:event_slug>/rsvps/<slug:rsvp_slug>/", views.rsvp_detail, name="rsvp-detail"),
    path("<slug:event_slug>/rsvps/<slug:rsvp_slug>/update/", views.rsvp_update, name="rsvp-update"),
    path("<slug:event_slug>/rsvps/<slug:rsvp_slug>/delete/", views.rsvp_delete, name="rsvp-delete"),
    path("<slug:event_slug>/rsvps/<slug:rsvp_slug>/success/", views.rsvp_success, name="rsvp-success"),
    path("<slug:event_slug>/rsvps/<slug:rsvp_slug>/cancel/", views.rsvp_cancel, name="rsvp-cancel")
]