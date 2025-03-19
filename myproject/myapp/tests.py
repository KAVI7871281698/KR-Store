from django.test import TestCase, Client
from django.urls import reverse
from .models import signup_page

class SignupViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        
        # Creating a user for duplicate email testing
        self.existing_user = signup_page.objects.create(
            fname="ExistingUser",
            email="existing@example.com",
            password="password123",
            address="123 Old Street",
            mobile="1234567890"
        )

    def test_signup_success(self):
        """Test successful registration with valid data"""
        response = self.client.post(self.signup_url, {
            'fname': 'NewUser',
            'email': 'newuser@example.com',
            'address': '456 New Street',
            'mobile': '0987654321',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to 'signin'
        self.assertTrue(signup_page.objects.filter(email='newuser@example.com').exists())

    def test_password_mismatch(self):
        """Test registration failure due to password mismatch"""
        response = self.client.post(self.signup_url, {
            'fname': 'TestUser',
            'email': 'testuser@example.com',
            'address': '789 Test Street',
            'mobile': '1234509876',
            'password': 'password123',
            'confirm_password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to 'signup'
        self.assertContains(response, 'Password does not match')
        self.assertFalse(signup_page.objects.filter(email='testuser@example.com').exists())

    def test_duplicate_email(self):
        """Test registration failure due to duplicate email"""
        response = self.client.post(self.signup_url, {
            'fname': 'AnotherUser',
            'email': 'existing@example.com',  # Already exists in the database
            'address': '123 Duplicate Street',
            'mobile': '1112223333',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to 'signin'
        self.assertContains(response, 'Email already exists')
        
    def test_get_signup_page(self):
        """Test loading the signup page successfully"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
