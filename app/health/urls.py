from django.urls import path
from . import views

urlpatterns = [
    # health home
    path("", views.index, name="health-home"),
    path("strength/", views.strength_index, name="strength-home"),
    path("nutrition/", views.nutrition_index, name="nutrition-home"),
    path("mental/", views.mental_index, name="mental-home"),

    # movements

    # exercises

    # plans
    path("plans/", views.plan_list, name="plan-list"),
    path("plans/create/", views.plan_create, name="plan-create"),
    path("plans/<slug:slug>/", views.plan_detail, name="plan-detail"),
    path("plans/<slug:slug>/update/", views.plan_update, name="plan-update"),
    path("plans/<slug:slug>/delete/", views.plan_delete, name="plan-delete"),
    path("plans/<slug:slug>/quick-action/<str:action>/", views.quick_action, name="quick-action"),

    # clients 
    path("clients/", views.client_list, name='client-list'),
    path("clients/<int:client_id>/", views.client_detail, name='client-detail'),
    path("clients/<str:trainer_username>/<str:client_username>/add/", views.client_add, name='client-add'),
    path("clients/<str:client_username>/remove/", views.client_remove, name='client-remove'),

    # client health profiles
    path("clients/<int:client_id>/create-health-profile/", views.create_health_profile, name='create-health-profile'),
    path("clients/<int:client_id>/update-health-profile/", views.update_health_profile, name='update-health-profile'),
    path('clients/update-profile/', views.update_profile, name='update_profile'),
]