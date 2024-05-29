from django.test import TestCase
from django.utils import timezone
from events.models import Event, Rsvp
import uuid

class EventModelTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Test Event",
            description="This is a test event",
            event_type="camp",
            start_date=timezone.now() + timezone.timedelta(days=1),
            end_date=timezone.now() + timezone.timedelta(days=2),
            location="Test Location"
        )

    def test_event_creation(self):
        self.assertTrue(isinstance(self.event, Event))
        self.assertEqual(self.event.__str__(), self.event.name)

    def test_slug_generation(self):
        self.event.save()
        self.assertIsNotNone(self.event.slug)

class RsvpModelTest(TestCase):
    def setUp(self):
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

    def test_rsvp_creation(self):
        self.assertTrue(isinstance(self.rsvp, Rsvp))
        self.assertEqual(self.rsvp.__str__(), f'{self.rsvp.name} - {self.event.name}')

    def test_slug_generation(self):
        self.event.save()
        self.assertIsNotNone(self.event.slug)