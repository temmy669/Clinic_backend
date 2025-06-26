from django.db import models
import uuid
from django.db import models

# Create your models here.
class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    reason = models.TextField(blank=True, null=True)
    preferred_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.preferred_date}"



