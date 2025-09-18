"""
Serializers for profiles app.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, EmailVerification, PhoneVerification
from .tasks import send_verification_email, send_otp_sms, send_welcome_email
import uuid


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "role",
            "address",
            "about_me",
        )
        extra_kwargs = {
            "email": {"required": False},
            "phone_number": {"required": False},
        }

    def validate(self, attrs):
        """Validate registration data."""
        if not attrs.get("email") and not attrs.get("phone_number"):
            raise serializers.ValidationError(
                "Either email or phone number must be provided."
            )

        if attrs.get("password") != attrs.get("password_confirm"):
            raise serializers.ValidationError("Passwords don't match.")

        return attrs

    def create(self, validated_data):
        """Create new user."""
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)

        # Send verification email if email provided
        if user.email:
            verification = EmailVerification.objects.create(user=user)
            verification_url = (
                f"http://localhost:3000/verify-email/{verification.token}/"
            )
            send_verification_email.delay(user.id, verification_url)

        # Send welcome email
        if user.email:
            send_welcome_email.delay(user.id)

        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email_or_phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        """Validate login credentials."""
        email_or_phone = attrs.get("email_or_phone")
        password = attrs.get("password")

        if email_or_phone and password:
            user = authenticate(
                request=self.context.get("request"),
                username=email_or_phone,
                password=password,
            )

            if not user:
                raise serializers.ValidationError("Invalid credentials.")

            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")

            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include email/phone and password.")


class OTPLoginSerializer(serializers.Serializer):
    """Serializer for OTP-based login."""

    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        """Validate phone number format."""
        if not value.startswith("+"):
            raise serializers.ValidationError(
                "Phone number must include country code (e.g., +1234567890)"
            )
        return value

    def create(self, validated_data):
        """Generate and send OTP."""
        phone_number = validated_data["phone_number"]

        # Get or create user
        user, created = User.objects.get_or_create(
            phone_number=phone_number, defaults={"role": "Customer"}
        )

        # Generate OTP
        import random

        otp_code = str(random.randint(100000, 999999))

        # Create phone verification record
        PhoneVerification.objects.create(
            user=user, phone_number=phone_number, otp_code=otp_code
        )

        # Send OTP via SMS
        send_otp_sms.delay(phone_number, otp_code)

        return {"message": "OTP sent successfully", "phone_number": phone_number}


class OTPVerifySerializer(serializers.Serializer):
    """Serializer for OTP verification."""

    phone_number = serializers.CharField(max_length=15)
    otp_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        """Validate OTP code."""
        phone_number = attrs.get("phone_number")
        otp_code = attrs.get("otp_code")

        try:
            verification = PhoneVerification.objects.filter(
                phone_number=phone_number, otp_code=otp_code, is_verified=False
            ).latest("created_at")

            # Check if OTP is not expired (10 minutes)
            from django.utils import timezone
            from datetime import timedelta

            if verification.created_at < timezone.now() - timedelta(minutes=10):
                raise serializers.ValidationError("OTP has expired.")

            verification.is_verified = True
            verification.save()

            attrs["user"] = verification.user
            return attrs

        except PhoneVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP code.")


class EmailVerificationSerializer(serializers.Serializer):
    """Serializer for email verification."""

    token = serializers.UUIDField()

    def validate_token(self, value):
        """Validate verification token."""
        try:
            verification = EmailVerification.objects.get(token=value, is_used=False)

            # Check if token is not expired (24 hours)
            from django.utils import timezone
            from datetime import timedelta

            if verification.created_at < timezone.now() - timedelta(hours=24):
                raise serializers.ValidationError("Verification token has expired.")

            return value

        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token.")

    def save(self):
        """Mark email as verified."""
        token = self.validated_data["token"]
        verification = EmailVerification.objects.get(token=token)
        verification.is_used = True
        verification.save()

        user = verification.user
        user.is_verified = True
        user.save()

        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for profile updates."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "about_me",
            "profile_picture",
            "role",
        )
        read_only_fields = ("id", "role", "email", "phone_number")

    def update(self, instance, validated_data):
        """Update user profile."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserDashboardSerializer(serializers.ModelSerializer):
    """Serializer for user dashboard data."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "address",
            "about_me",
            "profile_picture",
            "is_verified",
            "date_joined",
        )


class PublicUserProfileSerializer(serializers.ModelSerializer):
    """Serializer for public user profiles."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "role",
            "about_me",
            "profile_picture",
            "date_joined",
        )


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        """Validate password change data."""
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs

    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self):
        """Update user password."""
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    """Serializer for user logout."""

    refresh = serializers.CharField()

    def validate(self, attrs):
        """Validate refresh token."""
        from rest_framework_simplejwt.tokens import RefreshToken

        try:
            token = RefreshToken(attrs["refresh"])
            token.blacklist()
        except Exception:
            raise serializers.ValidationError("Invalid refresh token.")

        return attrs
