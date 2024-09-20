from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_events, name="list_events"),
    path("submit_event/", views.submit_event, name="submit_event"),

    # Submissions
    path("submissions/", views.list_submissions, name="list_submissions"),
    path('submissions/<int:submission_id>/<str:action>/', views.update_submission_status, name='update_submission_status'),
]