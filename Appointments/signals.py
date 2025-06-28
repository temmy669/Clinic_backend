from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Appointment
from .utils import (
    send_appointment_confirmation_email,
    send_reschedule_requested_email,
    send_cancellation_confirmation_email,
)

@receiver(pre_save, sender=Appointment)
def send_confirmation_on_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New appointment (no old status to compare)

    try:
        old_status = Appointment.objects.get(pk=instance.pk).status
    except Appointment.DoesNotExist:
        return  # Just in case

    new_status = instance.status

    if old_status != new_status:
        if new_status == 'confirmed':
            send_appointment_confirmation_email(instance)
        elif new_status == 'to-be-rescheduled':
            send_reschedule_requested_email(instance)
        elif new_status == 'cancelled':
            send_cancellation_confirmation_email(instance)