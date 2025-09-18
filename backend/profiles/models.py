from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, role=None, **extra_fields):
        """
        Create and return a user with email or phone number, password, and role.
        At least one of email or phone number must be provided.
        """
        if not email and not phone_number:
            raise ValueError("You can only use an email or a phone number.")

        # Normalize the email if provided
        email = self.normalize_email(email) if email else None

        # Create the user object
        user = self.model(
            email=email,
            phone_number=phone_number,
            role=role,
            **extra_fields
        )

        # Set the user's password securely
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def get_full_name(self):
        """Returns the user's full name if available, otherwise email/phone"""
        name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return name or self.email or self.phone_number

    def get_role_display_color(self):
        """Returns Tailwind color class based on role"""
        color_map = {
            'Fashion_Designer': 'purple',
            'Tailor': 'blue', 
            'Vendor': 'green',
            'Customer': 'gray',
            'Admin': 'red'
        }
        return color_map.get(self.role, 'gray')


    def create_superuser(self, email=None, password = None, phone_number=None, **extra_fields):
        """
        create and return a superuser with admin privilleges.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
    
        return self.create_user(email=email, password=password, phone_number=phone_number, **extra_fields)
    
# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    # Define roles for the user
    ROLE_CHOICES = (
        ("Customer", "Customer"),
        ("Fashion_Designer", "Fashion Designer"),
        ("Tailor", "Tailor"),
        ("Vendor", "Vendor"),
        ("Admin", "Admin"), # Admin role for superusers
    )

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True) #Email field (Unique)
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True) # Phone number field is unique
    address = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES) #Role field (choices are Customer, Tailor, Fashion Designer, Vendor)
    is_active = models.BooleanField(default=True) # To show if user is active
    is_staff = models.BooleanField(default=False) #To show if user is a staff
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Optional image field
    about_me = models.TextField(
        null=True, blank=True, 
        help_text="Please provide a brief description of yourself, including years of experience and expertise (especially for Tailors/Fashion Designers)."
    )
    
    # Use UserManager to handle User Creation
    objects = UserManager()

    # Define email as the username field
    USERNAME_FIELD = "email" # Email is the login identifier
    REQUIRED_FIELDS = ["role"] # This is required when creating a user

    def __str__(self):
        """
        Return a string represenative of the user, showing email or phone number.
        """
        return self.email if self.email else self.phone_number # show either email or phone number