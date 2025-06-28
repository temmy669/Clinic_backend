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


def send_appointment_confirmation_email(appointment):
    subject = 'Appointment Confirmed - Dental Clinic'

    cancel_url = f"http://your-frontend.com/cancel/{appointment.id}/"
    reschedule_url = f"http://your-frontend.com/reschedule/{appointment.id}/"

    message = (
        f"Hello {appointment.full_name},\n\n"
        f"Your appointment has been confirmed for {appointment.preferred_date}.\n"
        f"If you need to cancel or reschedule, use the links below:\n\n"
        f"Cancel: {cancel_url}\n"
        f"Reschedule: {reschedule_url}\n\n"
        f"Thank you,\nDental Clinic"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [appointment.email],
        fail_silently=False,
    )


def send_reschedule_requested_email(appointment):
    # Placeholder
    subject = "Appointment Reschedule Request - Dental Clinic"
    message = (
        f"Hello {appointment.full_name},\n\n"
        f"The clinic has requested to reschedule your appointment originally booked for {appointment.preferred_date}.\n"
        f"Please reach out or click the reschedule link to pick a new date.\n\n"
        f"Thank you,\nDental Clinic"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [appointment.email])


def send_cancellation_confirmation_email(appointment):
    subject = "Appointment Cancelled - Dental Clinic"
    message = (
        f"Hello {appointment.full_name},\n\n"
        f"Your appointment scheduled for {appointment.preferred_date} has been cancelled.\n"
        f"Please contact us if you'd like to rebook.\n\n"
        f"Thank you,\nDental Clinic"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [appointment.email])




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
