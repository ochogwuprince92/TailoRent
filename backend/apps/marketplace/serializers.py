from rest_framework import serializers
from .models import Product, Service, StyleFeed

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'vendor', 'name', 'description', 'price', 'image', 'created_at']
        read_only_fields = ['vendor', 'created_at']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'provider', 'title', 'description', 'price', 'available', 'created_at']
        read_only_fields = ['provider', 'created_at']

class StyleFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleFeed
        fields = ['id', 'user', 'image', 'caption', 'created_at']
        read_only_fields = ['user', 'created_at']