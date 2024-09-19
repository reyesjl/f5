from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="health-index"),
    path("request-trainer/<str:trainer_name>/", views.request_trainer, name="request-trainer")
]