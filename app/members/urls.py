from django.urls import path
from . import views

urlpatterns = [
    # Members
    path("", views.member_list, name="member-list"),

    # Authorization
    path("signup/", views.member_signup, name="member-signup"),
    path("login/", views.member_login, name="member-login"),
    path("logout/", views.member_logout, name="member-logout"),

    # Dashboards & public profile
    path("<str:username>/profile/", views.member_profile, name="member-profile"),
    path("<str:username>/dashboard/", views.member_dashboard, name="member-dashboard"),
    path("admin/<str:username>/dashboard/", views.admin_dashboard, name="admin-dashboard"),
    path("trainer/<str:username>/dashboard/", views.trainer_dashboard, name="trainer-dashboard"),
    path("player/<str:username>/dashboard/", views.player_dashboard, name="player-dashboard"),

    # Management
    #path("<str:username>/roles/", views.member-edit),
]