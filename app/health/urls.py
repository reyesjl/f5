from django.urls import path
from . import views

urlpatterns = [
    # health home
    path("", views.index, name="health-home"),
    path("strength/", views.strength_index, name="strength-home"),
    path("nutrition/", views.nutrition_index, name="nutrition-home"),
    path("mental/", views.mental_index, name="mental-home"),

    # plans
    path("plans/", views.plan_list, name="plan-list"),
    path("plans/create/", views.plan_create, name="plan-create"),
    path("plans/<slug:slug>/", views.plan_detail, name="plan-detail"),
    path("plans/<slug:slug>/update/", views.plan_update, name="plan-update"),
    path("plans/<slug:slug>/delete/", views.plan_delete, name="plan-delete"),
    
    # plan quick actions
    path("plans/<slug:slug>/quick-action/<str:action>/", views.quick_action, name="quick-action"),
]