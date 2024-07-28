from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Members
    path("", views.member_list, name="member-list"),

    # Authorization
    path("signup/", views.member_signup, name="member-signup"),
    path("login/", views.member_login, name="member-login"),
    path("logout/", views.member_logout, name="member-logout"),

    # Support
    path("login-support/", views.member_login_support, name="member-login-support"),
    path("support/support-form/", views.member_support_form, name="member-support-form"),
    path("support/support-success/", views.member_support_success, name="member-support-success"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='members/registration/password_reset_form.html'), name='password-reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='members/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='members/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='members/registration/password_reset_complete.html'), name='password_reset_complete'),

    # Dashboards & public profile
    path("<str:username>/detail/", views.member_detail, name="member-detail"),
    path("<str:username>/update/", views.member_update, name="member-update"),
    path("<str:username>/profile/", views.member_profile, name="member-profile"),
    path("dashboard/", views.member_dashboard, name="member-dashboard"),

    # Management
    #path("<str:username>/roles/", views.member-edit),
]