from django.urls import path
from . import views

urlpatterns = [
    # health home
    path("", views.index, name="health-index"),
    path("strength/", views.strength_index, name="strength-home"),
    path("nutrition/", views.nutrition_index, name="nutrition-home"),
    path("mental/", views.mental_index, name="mental-home"),

    # plans
    path("plans/", views.plan_list, name="plan-list"),
    path("plans/create/", views.plan_create, name="plan-create"),
    path("plans/<slug:slug>/", views.plan_detail, name="plan-detail"),
    path("plans/<slug:slug>/update/", views.plan_update, name="plan-update"),
    path("plans/<slug:slug>/delete/", views.plan_delete, name="plan-delete"),

    # clients 
    path("clients/", views.client_list, name='client-list'),
    path("clients/<int:client_id>/", views.client_detail, name='client-detail'),
    path("clients/<str:trainer_username>/<str:client_username>/add/", views.client_add, name='client-add'),
    path("clients/<str:client_username>/remove/", views.client_remove, name='client-remove'),

    # request sessions
    path("trainers/<int:trainer_id>/request-session/", views.request_trainer_session, name='request-trainer-session'),
    path("trainer/request/<int:session_id>/approve/", views.approve_trainer_session, name="approve-trainer-session"),
    path("trainer/request/<int:session_id>/reset/", views.reset_trainer_session, name="reset-trainer-session"),
    path("trainer/request/<int:session_id>/reject/", views.reject_trainer_session, name="reject-trainer-session"),
    path("trainer/request/<int:session_id>/delete/", views.delete_trainer_session, name="delete-trainer-session"),
]