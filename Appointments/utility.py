from django.core.mail import send_mail
from django.conf import settings
from decouple import config
from twilio.rest import Client


#Email Notification
def notify_admin_of_new_appointment(appointment):
    subject = 'New Appointment Request'
    message = (
        f"A new appointment has been requested:\n\n"
        f"Name: {appointment.full_name}\n"
        f"Email: {appointment.email}\n"
        f"Phone: {appointment.phone}\n"
        f"Preferred Date: {appointment.preferred_date}\n"
        f"Reason: {appointment.reason or 'N/A'}\n"
    )

    admin_email = config('ADMIN_CONFIRMATION_EMAIL', default='your_admin_email')
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])


#SMS Notification
def send_sms_to_admin(appointment):
    account_sid = config('TWILIO_SID', default='your_twilio_sid')
    auth_token = config('TWILIO_AUTH_TOKEN', default='your_twilio_auth_token')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"New appointment: {appointment.full_name} - {appointment.preferred_date}",
        from_=config('TWILIO_NUMBER', default='your_twilio_number'),  # Twilio number
        to=config('ADMIN_PHONE_NUMBER', default='admin_phone_number')   # Admin phone number
    )
