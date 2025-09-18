# API VIEWS (DRF-based)
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import (
    RegistrationSerializer, LoginSerializer, LogoutSerializer,
    ProfileUpdateSerializer, UserDashboardSerializer, ChangePasswordSerializer,
    PublicUserProfileSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
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
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User logged out successfully."}, status=status.HTTP_204_NO_CONTENT)

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class DashboardView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserDashboardSerializer(user)
        return Response(serializer.data)

class ChangePasswordView(generics.UpdateAPIView):
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
    serializer_class = PublicUserProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.filter(role__in=['tailor', 'fashion_designer'], is_active=True)

# TEMPLATE VIEWS

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from profiles.models import User
from bookings.models import Booking
from marketplace.models import Product, Service
from marketplace.models import NewsfeedPost
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ProfileUpdateForm, LoginForm
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib import messages
from django.core.paginator import Paginator

def Signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

class CustomLoginView(DjangoLoginView):
    template_name = 'registration/login.html'

@login_required
def dashboard_view(request):
    user = request.user
    role = user.role

    # 1. Recent bookings for customers
    bookings = Booking.objects.filter(customer=user).order_by('-date')[:5] if role == "Customer" else None

    # 2. Recent listings for vendors or professionals
    listings = None
    if role == "Vendor":
        listings = Product.objects.filter(vendor=user).order_by('-created_at')[:5]
    elif role in ["Tailor", "Fashion_Designer"]:
        listings = Service.objects.filter(provider=user).order_by('-created_at')[:5]

    # 3. Recent accepted orders involving the user
    orders = Booking.objects.filter(
        status='accepted'
    ).filter(
        Q(customer=user) | Q(professional=user)
    ).order_by('-date')[:5]

    # 4. Discoverable professionals (for customers or vendors)
    professionals = []
    if role not in ["Tailor", "Fashion_Designer"]:
        professionals = User.objects.filter(
            role__in=["Tailor", "Fashion_Designer"],
            is_active=True
        ).exclude(id=user.id)[:5]

    # 5. Latest newsfeed posts
    newsfeed_posts = NewsfeedPost.objects.all().order_by('-created_at')[:5]

    # 6. Dashboard statistics
    total_bookings = Booking.objects.filter(customer=user).count() if role == "Customer" else 0
    total_listings = 0
    if role == "Vendor":
        total_listings = Product.objects.filter(vendor=user).count()
    elif role in ["Tailor", "Fashion_Designer"]:
        total_listings = Service.objects.filter(provider=user).count()

    # 7. Render dashboard template with all context data
    return render(request, 'dashboard.html', {
        'user': user,
        'role': role,
        'bookings': bookings,
        'listings': listings,
        'orders': orders,
        'professionals': professionals,
        'newsfeed_posts': newsfeed_posts,
        'highlights': {
            'total_bookings': total_bookings,
            'total_listings': total_listings,
        },
    })


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'profile_update.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')

def professional_list_view(request):
    professionals = User.objects.filter(role__in=["Tailor", "Fashion_Designer"], is_active=True)
    return render(request, 'professional_list.html', {'professionals': professionals})

def about_view(request):
    return render(request, 'about.html')

def custom_login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        identifier = form.cleaned_data.get('email_or_phone')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=identifier, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # or any other redirect
        else:
            form.add_error(None, 'Invalid email/phone or password')

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  

def newsfeed_view(request):
    posts_list = NewsfeedPost.objects.select_related('user').order_by('-created_at')
    
    # Paginate with 5 posts per page
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)  # Safe page object

    return render(request, 'newsfeed.html', {'posts': posts})

# view for professional detail
@login_required
def professional_detail_view(request, pk):
    professional = get_object_or_404(User, pk=pk, role__in=["Tailor", "Fashion_Designer"], is_active=True)
    return render(request, 'professional_detail.html', {'professional': professional})

def dashboard(request):
    context = {
        'professionals': User.objects.filter(
            role__in=['Fashion_Designer', 'Tailor']
        ).exclude(id=request.user.id)[:10] or [],
        'orders': Booking.objects.filter(
            customer=request.user
        ).order_by('-date')[:3] or [],
        'newsfeed_posts': NewsfeedPost.objects.all().order_by('-created_at')[:20] or [],
        'highlights': {
            'total_listings': Service.objects.count(),
            'total_bookings': Booking.objects.filter(customer=request.user).count()
        }
    }
    return render(request, 'dashboard.html', context)