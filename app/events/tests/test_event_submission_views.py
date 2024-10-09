from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import EventSubmission
from django.utils import timezone


class EventViewsTestCase(TestCase):

    def setUp(self):
        # Use the custom user model
        User = get_user_model()
        
        # Create test users
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword', is_staff=True)
        self.regular_user = User.objects.create_user(username='user', password='userpassword', is_staff=False)

    def test_event_submission_list_view_authenticated(self):
        """Test the Event Submission List view - should be accessible only to admin"""
        url = reverse('list_event_submissions')
        
        # Admin user can view submissions
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

    def test_event_submission_create_view(self):
        """Test the Event Submission Create view - should be accessible by anyone"""
        url = reverse('create_event_submission')
        data = {
            'event_name': 'Test Event Submission',
            'event_description': 'This is a test submission.',
            'event_date': timezone.now().date(),
            'name': 'Test Submitter',
            'email': 'test@example.com',
            'phone_number': '1234567890',
        }
        
        # Regular user can create a submission
        self.client.login(username='user', password='userpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Successful redirection (form submission)
        
        # Check if submission is created
        self.assertTrue(EventSubmission.objects.filter(name='Test Submitter').exists())