from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.member_signup, name="member-signup"),
    path("login/", views.member_login, name="member-login"),
    path("dashboard/<str:username>/", views.member_dashboard, name="member-dashboard"),
    path("admin/dashboard/<str:username>/", views.admin_dashboard, name="admin-dashboard"),
    path("trainer/dashboard/<str:username>/", views.trainer_dashboard, name="trainer-dashboard"),
    path("player/dashboard/<str:username>/", views.player_dashboard, name="player-dashboard"),
    path("logout/", views.member_logout, name="member-logout"),
]