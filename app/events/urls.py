from django.urls import path

from .views.event_views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView
from .views.event_submission_views import EventSubmissionListView, EventSubmissionCreateView


urlpatterns = [
    # Event URLs
    path('', EventListView.as_view(), name='list_events'),
    path('<int:pk>/', EventDetailView.as_view(), name='detail_event'),
    path('create/', EventCreateView.as_view(), name='create_event'),
    path('update/<int:pk>/', EventUpdateView.as_view(), name='update_event'),
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='delete_event'),

    # EventSubmission URLs
    path('submissions/', EventSubmissionListView.as_view(), name='list_event_submissions'),
    path('submissions/create/', EventSubmissionCreateView.as_view(), name='create_event_submission'),
]