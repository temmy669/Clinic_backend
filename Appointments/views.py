from django.shortcuts import render
from rest_framework import generics
from .models import Appointment
from .serializers import AppointmentSerializer
from .utility import *

# Create your views here.
class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        appointment = serializer.save()
        notify_admin_of_new_appointment(appointment)
        # send_sms_to_admin(appointment) 


