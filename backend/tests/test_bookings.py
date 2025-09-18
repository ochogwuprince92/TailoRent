"""
Tests for bookings app.
"""

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.bookings.models import Booking
from apps.profiles.models import User


class BookingModelTest(TestCase):
    """Test cases for Booking model."""

    def setUp(self):
        """Set up test data."""
        self.customer = User.objects.create_user(
            email="customer@example.com", password="testpass123", role="Customer"
        )
        self.tailor = User.objects.create_user(
            email="tailor@example.com", password="testpass123", role="Tailor"
        )

    def test_create_booking(self):
        """Test creating a booking."""
        booking = Booking.objects.create(
            customer=self.customer,
            professional=self.tailor,
            service_type="Suit Alteration",
            date="2024-01-15 10:00:00",
            location="123 Main St",
            notes="Please make it ready by next week",
        )
        self.assertEqual(booking.customer, self.customer)
        self.assertEqual(booking.professional, self.tailor)
        self.assertEqual(booking.service_type, "Suit Alteration")
        self.assertEqual(booking.status, "pending")

    def test_booking_str_representation(self):
        """Test booking string representation."""
        booking = Booking.objects.create(
            customer=self.customer,
            professional=self.tailor,
            service_type="Suit Alteration",
            date="2024-01-15 10:00:00",
        )
        expected = f"Booking by {self.customer} with {self.tailor} for Suit Alteration on 2024-01-15 10:00:00"
        self.assertEqual(str(booking), expected)


class BookingAPITest(APITestCase):
    """Test cases for Booking API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.customer = User.objects.create_user(
            email="customer@example.com", password="testpass123", role="Customer"
        )
        self.tailor = User.objects.create_user(
            email="tailor@example.com", password="testpass123", role="Tailor"
        )

    def test_create_booking_authenticated(self):
        """Test creating booking when authenticated."""
        self.client.force_authenticate(user=self.customer)
        url = reverse("bookings:booking-list")
        data = {
            "professional": self.tailor.id,
            "service_type": "Suit Alteration",
            "date": "2024-01-15T10:00:00Z",
            "location": "123 Main St",
            "notes": "Please make it ready by next week",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(customer=self.customer).exists())

    def test_create_booking_unauthenticated(self):
        """Test creating booking when not authenticated."""
        url = reverse("bookings:booking-list")
        data = {
            "professional": self.tailor.id,
            "service_type": "Suit Alteration",
            "date": "2024-01-15T10:00:00Z",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
