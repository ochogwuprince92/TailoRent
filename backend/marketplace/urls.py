from django.urls import path
from .views import (
    ProductListCreateView, ProductDetailView,
    ServiceListCreateView, ServiceDetailView, StyleFeedListCreateView, StyleFeedDetailView
    
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('style-feed/', StyleFeedListCreateView.as_view(), name='style-feed'),
    path('style-feed/<int:pk>/', StyleFeedDetailView.as_view(), name='style-feed-detail'),

]
