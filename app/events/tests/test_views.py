from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from events.models import Event, Rsvp
from django.contrib.auth.models import User, Group
from django.utils.http import urlencode
from unittest import skip

class EventViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.manager_group = Group.objects.create(name='event_manager')
        self.user.groups.add(self.manager_group)

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
        self.assertIn('events', response.context)
        self.assertQuerysetEqual(
            response.context['events'],
            Event.objects.upcoming().order_by('start_date'),
            transform=lambda x: x
        )

    def test_event_detail_view(self):
        response = self.client.get(reverse('event-detail', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_detail.html')
        self.assertIn('event', response.context)
        self.assertEqual(response.context['event'], self.event)

    def test_event_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('event-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_form.html')

        response = self.client.post(reverse('event-create'), {
            'name': 'New Event',
            'description': 'Description of new event',
            'event_type': 'camp',
            'start_date': timezone.now() + timezone.timedelta(days=3),
            'end_date': timezone.now() + timezone.timedelta(days=4),
            'location': 'New Location'
        })
        self.assertRedirects(response, reverse('event-list'))
        self.assertTrue(Event.objects.filter(name='New Event').exists())

    def test_event_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('event-update', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_update.html')

        response = self.client.post(reverse('event-update', args=[self.event.slug]), {
            'name': 'Updated Event',
            'description': 'Updated description',
            'event_type': 'camp',
            'start_date': self.event.start_date,
            'end_date': self.event.end_date,
            'location': self.event.location
        })
        self.assertRedirects(response, reverse('event-detail', args=[self.event.slug]))
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, 'Updated Event')

    def test_event_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('event-delete', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_delete_confirm.html')

        response = self.client.post(reverse('event-delete', args=[self.event.slug]))
        self.assertRedirects(response, reverse('event-list'))
        self.assertFalse(Event.objects.filter(slug=self.event.slug).exists())

class RsvpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.manager_group = Group.objects.create(name='event_manager')
        self.user.groups.add(self.manager_group)

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
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('rsvp-list', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rsvps/rsvp_list.html')
        self.assertIn('rsvps', response.context)
        self.assertQuerysetEqual(
            response.context['rsvps'],
            Rsvp.objects.by_event(self.event),
            transform=lambda x: x
        )

    def test_rsvp_create_view(self):
        response = self.client.get(reverse('rsvp-create', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rsvps/rsvp_form.html')

        response = self.client.post(reverse('rsvp-create', args=[self.event.slug]), {
            'name': 'New User',
            'email': 'newuser@example.com',
            'phone_number': '0987654321',
            'role': 'spectator'
        })
        self.assertRedirects(response, reverse('event-detail', args=[self.event.slug]))
        self.assertTrue(Rsvp.objects.filter(email='newuser@example.com').exists())

    def test_rsvp_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('rsvp-update', args=[self.event.slug, self.rsvp.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rsvps/rsvp_update.html')

        response = self.client.post(reverse('rsvp-update', args=[self.event.slug, self.rsvp.slug]), {
            'name': 'Updated User',
            'email': self.rsvp.email,
            'phone_number': self.rsvp.phone_number,
            'role': self.rsvp.role
        })
        self.assertRedirects(response, reverse('rsvp-detail', args=[self.event.slug, self.rsvp.slug]))
        self.rsvp.refresh_from_db()
        self.assertEqual(self.rsvp.name, 'Updated User')

    @skip("Not Implemented Yet")
    def test_rsvp_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('rsvp-delete', args=[self.event.slug, self.rsvp.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rsvps/rsvp_delete_confirm.html')

        response = self.client.post(reverse('rsvp-delete', args=[self.event.slug, self.rsvp.slug]))
        self.assertRedirects(response, reverse('rsvp-list', args=[self.event.slug]))
        self.assertFalse(Rsvp.objects.filter(slug=self.rsvp.slug).exists())