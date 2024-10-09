from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import Event
from django.utils import timezone


class EventViewsTestCase(TestCase):

    def setUp(self):
        # Use the custom user model
        User = get_user_model()
        
        # Create test users
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword', is_staff=True)
        self.regular_user = User.objects.create_user(username='user', password='userpassword', is_staff=False)
        
        # Create an event
        self.event = Event.objects.create(
            name='Test Event',
            description='This is a test event.',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(hours=1),
            location='Test Location'
        )

    def test_event_list_view(self):
        """Test the Event List view - should be accessible to all users"""
        url = reverse('list_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/list_events.html')
        self.assertContains(response, 'Test Event')

    def test_event_create_view_authenticated(self):
        """Test the Event Create view - should only be accessible to admin users"""
        url = reverse('create_event')
        
        # Admin user can create
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Non-admin user should be redirected (302)
        self.client.logout()
        self.client.login(username='user', password='userpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # Optionally, check if it redirects to login page
        self.assertRedirects(response, '/members/login/?next=' + url)

    def test_event_detail_view(self):
        """Test the Event Detail view"""
        url = reverse('detail_event', args=[self.event.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/detail_event.html')
        self.assertContains(response, 'Test Event')

    def test_event_update_view_authenticated(self):
        """Test the Event Update view - should only be accessible to admin users"""
        url = reverse('update_event', args=[self.event.pk])
        
        # Admin user can update
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Non-admin user should be redirected (302)
        self.client.logout()
        self.client.login(username='user', password='userpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # Optionally, check if it redirects to login page
        self.assertRedirects(response, '/members/login/?next=' + url)

    def test_event_delete_view_authenticated(self):
        """Test the Event Delete view - should only be accessible to admin users"""
        url = reverse('delete_event', args=[self.event.pk])
        
        # Admin user can delete
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Non-admin user should be redirected (302)
        self.client.logout()
        self.client.login(username='user', password='userpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # Optionally, check if it redirects to login page
        self.assertRedirects(response, '/members/login/?next=' + url)
