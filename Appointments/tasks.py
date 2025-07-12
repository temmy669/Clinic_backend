from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from .models import Appointment


@shared_task
def send_appointment_reminders():
    now = datetime.now()
    
    #24 hour reminder window
    reminder_time_start_24 = now + timedelta(hours=24)
    reminder_time_end_24= reminder_time_start_24 + timedelta(minutes=5)  # 5-min buffer window

    #4 hour reminder window
    reminder_time_start_4 = now + timedelta(hours=4)
    reminder_time_end_4 = reminder_time_start_4 + timedelta(minutes=5)  # 5-min buffer window


    # Find appointments happening exactly ~24 hours from now
    upcoming_24 = Appointment.objects.filter(
        status='confirmed',
        hr24_reminder_sent=False,
        preferred_date__range=(reminder_time_start_24, reminder_time_end_24)
    )

    for appt in upcoming_24:
        send_mail(
            subject='Reminder: Upcoming Appointment',
            message=(
                f"Hi {appt.full_name},\n\n"
                f"This is a reminder that you have a dental appointment scheduled for tomorrow,"
                f"{appt.preferred_date} at {appt.preferred_time}.\n\n"
                "Please ensure to arrive 10 minutes earlier than your scheduled time.\n\nThank you!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appt.email],
            fail_silently=False
        )
        #Mark the appointment reminder as sent
        appt.hr24_reminder_sent = True
        appt.save()
        
        
    # Find appointments happening exactly ~4 hours from now
    upcoming_4 = Appointment.objects.filter(
        status='confirmed',
        hr4_reminder_sent=False,
        preferred_date__range=(reminder_time_start_4, reminder_time_end_4)
    )
    
    for appt in upcoming_4:
        send_mail(
            subject='Reminder: Upcoming Appointmtnt',
            message=(
                f'Hi {appt.full_name},\n\n'
                f'This is a reminder that you have a dental appointment scheduled for today, at '
                f'{appt.preferred_time.strftime("%I:%M %p").lstrip("0") if appt.preferred_time else "an unspecified time"}'
            ),
             from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appt.email],
            fail_silently=False
        )
        #Mark the appointment reminder as sent
        appt.hr4_reminder_sent = True
        appt.save()        
        
        
                
        
        
