"""
Pytest configuration and fixtures for TailoRent tests.
"""

import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from apps.profiles.models import User

User = get_user_model()


@pytest.fixture
def client():
    """Django test client fixture."""
    return Client()


@pytest.fixture
def user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "phone_number": "1234567890",
        "password": "testpass123",
        "role": "Customer",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def customer_user(user_data):
    """Create a customer user for testing."""
    user = User.objects.create_user(**user_data)
    return user


@pytest.fixture
def tailor_user():
    """Create a tailor user for testing."""
    return User.objects.create_user(
        email="tailor@example.com",
        phone_number="0987654321",
        password="testpass123",
        role="Tailor",
        first_name="John",
        last_name="Tailor",
    )


@pytest.fixture
def fashion_designer_user():
    """Create a fashion designer user for testing."""
    return User.objects.create_user(
        email="designer@example.com",
        phone_number="1122334455",
        password="testpass123",
        role="Fashion_Designer",
        first_name="Jane",
        last_name="Designer",
    )


@pytest.fixture
def vendor_user():
    """Create a vendor user for testing."""
    return User.objects.create_user(
        email="vendor@example.com",
        phone_number="5566778899",
        password="testpass123",
        role="Vendor",
        first_name="Bob",
        last_name="Vendor",
    )


@pytest.fixture
def admin_user():
    """Create an admin user for testing."""
    return User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass123",
        role="Admin",
    )
