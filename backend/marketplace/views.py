from rest_framework import generics, permissions, filters
from .models import Product, Service,  StyleFeed
from .serializers import ProductSerializer, ServiceSerializer, StyleFeedSerializer
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']



# --- Product Views ---
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role != 'vendor':
            raise PermissionDenied("Only vendors can list products.")
        serializer.save(vendor=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user)


# --- Service Views ---
class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Service.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role not in ['tailor', 'fashion_designer']:
            raise PermissionDenied("Only tailors or fashion designers can offer services.")
        serializer.save(professional=self.request.user)

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(professional=self.request.user)

class StyleFeedListCreateView(generics.ListCreateAPIView):
    queryset = StyleFeed.objects.all().order_by('-created_at')
    serializer_class = StyleFeedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StyleFeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StyleFeed.objects.all()
    serializer_class = StyleFeedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return StyleFeed.objects.all().order_by('-created_at')