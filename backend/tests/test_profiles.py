"""
Tests for profiles app.
"""

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.profiles.models import User
from apps.profiles.serializers import RegistrationSerializer


class UserModelTest(TestCase):
    """Test cases for User model."""

    def test_create_user_with_email(self):
        """Test creating user with email."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123", role="Customer"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertEqual(user.role, "Customer")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_with_phone(self):
        """Test creating user with phone number."""
        user = User.objects.create_user(
            phone_number="1234567890", password="testpass123", role="Tailor"
        )
        self.assertEqual(user.phone_number, "1234567890")
        self.assertTrue(user.check_password("testpass123"))
        self.assertEqual(user.role, "Tailor")

    def test_create_superuser(self):
        """Test creating superuser."""
        user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123", role="Admin"
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_str_representation(self):
        """Test user string representation."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123", role="Customer"
        )
        self.assertEqual(str(user), "test@example.com")


class ProfileAPITest(APITestCase):
    """Test cases for Profile API endpoints."""

    def test_user_registration(self):
        """Test user registration endpoint."""
        url = reverse("profiles:register")
        data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "role": "Customer",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_user_login(self):
        """Test user login endpoint."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123", role="Customer"
        )
        url = reverse("profiles:login")
        data = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_update(self):
        """Test profile update endpoint."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123", role="Customer"
        )
        self.client.force_authenticate(user=user)

        url = reverse("profiles:profile-update")
        data = {"first_name": "Updated", "last_name": "Name"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.last_name, "Name")
