from rest_framework import serializers
from .models import User
# To create LoginSerializer, you need to import the following
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,  TokenError
from django.contrib.auth.password_validation import validate_password


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Takes input from email/phone, password and role.
    It also securely hashes the password before saving the user
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'location', 'role', 'password', 'confirm_password', 'profile_picture', 'about_me']

    def validate(self, data):
        """
        Ensure the password and confirm_password match.
        """
        password = data.get('password')
        confirm_password = data.get('confirm_password')
            
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        return data
    
    def create(self, validated_data):
        """
        Create and return a user instance.
        """
        validated_data.pop('confirm_password')  # Remove confirm_password before creating the user
        user = User.objects.create_user(**validated_data)
        return user
    
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login using either email or phone number and password.
    """

    email = serializers.EmailField(required=False)  # Make optional
    phone_number = serializers.CharField(required=False)  # Make optional
    password = serializers.CharField(required=True, write_only=True)  # Password must be provided

    def validate(self, data):
        """
        Validate the user credentials and return JWT tokens on success.
        """
        email = data.get("email",)
        phone_number = data.get("phone_number",)
        password = data.get("password")

        # Make sure either email or phone_number is provided
        if not email and not phone_number:
            raise serializers.ValidationError("Either email or phone number is required.")

        # Try to find user either by email or phone number
        user = None
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist.")
        elif phone_number:
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this phone number does not exist.")

        # Check password
        if user and not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        # Check if user is active
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # If all is good, generate tokens
        refresh = RefreshToken.for_user(user)

        # Return both user info and tokens
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user,  # Pass user back for the view
            'user_id': user.id,
            'email': user.email,
            'phone_number': user.phone_number,
            'role': user.role,
        }


# Create Logout serializers
class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logout. Only validates that refresh token is provided.
    """
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()  # Blacklist the refresh token
        except TokenError:
            self.fail('bad_token')

# Create update serializers for the user
class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating user profile
    """
    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone_number', 'first_name', 'last_name', 'location', 'profile_picture', 'about_me', 'date_joined'
        ]
        read_only_fields = ['id', 'email', 'phone_number',  'role', 'date_joined']

# Create a serializer for the user dashboard
class UserDashboardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'location',
            'profile_picture',
            'about_me',
            'date_joined',
        ]
# Create a serializer to change the password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user

        # Check old password
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is not correct."})

        # Check new password match
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user
 
class PublicUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'about_me', 'location', 'profile_picture']