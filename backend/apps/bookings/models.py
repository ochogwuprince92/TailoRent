from django.db import models
from django.conf import settings

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="bookings", on_delete=models.CASCADE)
    professional = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="services_offered", on_delete=models.CASCADE)
    service_type = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True) 
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Booking by {self.customer} with {self.professional} for {self.service_type} on {self.date}"
