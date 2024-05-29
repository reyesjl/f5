from django.test import TestCase, Client
from django.urls import reverse
from events.models import Event, Rsvp
from django.utils import timezone

class EventViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(
            name="Test Event",
            description="This is a test event",
            event_type="camp",
            start_date=timezone.now() + timezone.timedelta(days=1),
            end_date=timezone.now() + timezone.timedelta(days=2),
            location="Test Location"
        )

    def test_event_list_view(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_list.html')

    def test_event_detail_view(self):
        response = self.client.get(reverse('event-detail', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_detail.html')

    def test_event_create_view(self):
        response = self.client.get(reverse('event-create'))
        self.assertEqual(response.status_code, 403)  # Assuming user must be logged in

class RsvpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(
            name="Test Event",
            description="This is a test event",
            event_type="camp",
            start_date=timezone.now() + timezone.timedelta(days=1),
            end_date=timezone.now() + timezone.timedelta(days=2),
            location="Test Location"
        )
        self.rsvp = Rsvp.objects.create(
            event=self.event,
            name="Test User",
            email="testuser@example.com",
            phone_number="1234567890",
            role="player"
        )

    def test_rsvp_list_view(self):
        response = self.client.get(reverse('rsvp-list', args=[self.event.slug]))
        self.assertEqual(response.status_code, 403)  # Assuming user must be logged in

    def test_rsvp_create_view(self):
        response = self.client.get(reverse('rsvp-create', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rsvps/rsvp_form.html')