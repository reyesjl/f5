from django.test import TestCase
from events.forms import EventForm, RsvpForm, RsvpFormNoPayment
from events.models import Event
from django.utils import timezone

class EventFormTest(TestCase):
    def test_event_form_valid_data(self):
        form = EventForm(data={
            'name': 'Test Event',
            'description': 'This is a test event',
            'event_type': 'camp',
            'start_date': timezone.now() + timezone.timedelta(days=1),
            'end_date': timezone.now() + timezone.timedelta(days=2),
            'location': 'Test Location',
        })
        self.assertTrue(form.is_valid())

    def test_event_form_invalid_data(self):
        form = EventForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)  # Adjust the number of expected errors

class RsvpFormTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Test Event",
            description="This is a test event",
            event_type="camp",
            start_date=timezone.now() + timezone.timedelta(days=1),
            end_date=timezone.now() + timezone.timedelta(days=2),
            location="Test Location"
        )

    def test_rsvp_form_valid_data(self):
        form = RsvpForm(data={
            'name': 'Test User',
            'email': 'testuser@example.com',
            'phone_number': '1234567890',
            'role': 'player',
            'credit_card_number': '1234567812345678',
            'full_name_on_card': 'Test User',
            'expiration_month': '12',
            'expiration_year': '2025',
            'cvv': '123',
        }, event=self.event)
        self.assertTrue(form.is_valid())

    def test_rsvp_form_invalid_data(self):
        form = RsvpForm(data={}, event=self.event)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 9)  # Adjust the number of expected errors

class RsvpFormNoPaymentTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Test Event",
            description="This is a test event",
            event_type="camp",
            start_date=timezone.now() + timezone.timedelta(days=1),
            end_date=timezone.now() + timezone.timedelta(days=2),
            location="Test Location"
        )

    def test_rsvp_form_no_payment_valid_data(self):
        form = RsvpFormNoPayment(data={
            'name': 'Test User',
            'email': 'testuser@example.com',
            'phone_number': '1234567890',
            'role': 'player'
        }, event=self.event)
        self.assertTrue(form.is_valid())

    def test_rsvp_form_no_payment_invalid_data(self):
        form = RsvpFormNoPayment(data={}, event=self.event)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # Adjust the number of expected errors
