from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="health_index"),
    path("request_trainer/<str:trainer_name>/", views.request_trainer, name="request_trainer")
]