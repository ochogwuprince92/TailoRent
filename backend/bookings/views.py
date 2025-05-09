from rest_framework import generics, permissions, status, views
from .models import Booking
from .serializers import BookingSerializer, BookingStatusUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class BookingListCreateView(generics.ListCreateAPIView):
    """
    Allows a customer to create and view their own bookings.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class ProfessionalBookingsView(generics.ListAPIView):
    """
    Allows a tailor or fashion designer to view all bookings made to them.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(professional=self.request.user)
    

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific booking (by the customer).
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)
    
class UpdateBookingStatusView(generics.UpdateAPIView):
    """
    Allows a provider (tailor/fashion designer) to update booking status.
    """
    serializer_class = BookingStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(provider=self.request.user)
    
class ProfessionalDashboardView(views.APIView):
    """
    Dashboard view for tailors/fashion designers to see their activity.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Only allow for professionals
        if user.role not in ['tailor', 'fashion_designer']:
            return Response({"detail": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

        bookings = Booking.objects.filter(provider=user)
        data = {
            "id": user.id,
            "email": user.email,
            "full_name": f"{user.first_name} {user.last_name}",
            "role": user.role,
            "total_bookings": bookings.count(),
            "accepted_bookings": bookings.filter(status='accepted').count(),
            "rejected_bookings": bookings.filter(status='rejected').count(),
            "pending_bookings": bookings.filter(status='pending').count(),
        }

        return Response(data, status=status.HTTP_200_OK)
    
class CustomerDashboardView(APIView):
    """
    Returns a summary of the customer's booking activity.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Confirm user is a customer
        if user.role != 'customer':
            return Response({"detail": "You are not authorized to access this dashboard."}, status=403)

        total_bookings = Booking.objects.filter(customer=user).count()
        pending = Booking.objects.filter(customer=user, status='pending').count()
        accepted = Booking.objects.filter(customer=user, status='accepted').count()
        rejected = Booking.objects.filter(customer=user, status='rejected').count()

        return Response({
            "total_bookings": total_bookings,
            "pending": pending,
            "accepted": accepted,
            "rejected": rejected,
        })