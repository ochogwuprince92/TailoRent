from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer, ProfileUpdateSerializer, UserDashboardSerializer, ChangePasswordSerializer, PublicUserProfileSerializer
from rest_framework.permissions import AllowAny
from .models import User

class RegistrationView(generics.GenericAPIView):
    """
    View for registering new users (signup).
    """
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny] # Anyone can register

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to register a new user.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "role": user.role,
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(generics.GenericAPIView):
    """
    View for user login.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]  # Anyone (even unauthenticated) can attempt login

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to login a user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate user input
        
        # Get validated data
        data = serializer.validated_data

        return Response({
            "message": "User logged in successfully",
            "refresh": data['refresh'],
            "access": data['access'],
            "user": {
                "id": data['user_id'],
                "email": data['email'],
                "phone_number": data['phone_number'],
                "role": data['role'],
            }
        }, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    """
    View for user logout.
    """
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can logout

    
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to logout user (blacklist token).
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "User logged out successfully."}, status=status.HTTP_204_NO_CONTENT)
   
# View for updating user profile
class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating the logged-in user's profile.
    """
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Return the current authenticated user
        """
        return self.request.user
    

# create a dashboard view
class DashboardView(generics.RetrieveAPIView):
    """
    Dashboard/Homepage view for the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserDashboardSerializer(user)
        return Response(serializer.data)

# Create a view to change the password
class ChangePasswordView(generics.UpdateAPIView):
    """
    Allow authenticated users to change their password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

class ProfessionalListView(generics.ListAPIView):
    """
    List all active professionals (tailors or fashion designers).
    """
    serializer_class = PublicUserProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.filter(role__in=['tailor', 'fashion_designer'], is_active=True)