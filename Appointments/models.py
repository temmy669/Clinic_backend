from django.db import models
import uuid
from django.db import models

# Create your models here.

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('to-be-rescheduled', 'To be Rescheduled'),
]


class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    reason = models.TextField(blank=True, null=True)
    preferred_date = models.DateField()
    preferred_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_cancelled = models.BooleanField(default=False)
    hr24_reminder_sent = models.BooleanField(default=False)
    hr4_reminder_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.full_name} - {self.preferred_date}"



