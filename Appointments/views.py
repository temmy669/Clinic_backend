from django.shortcuts import render
from rest_framework import generics
from .models import Appointment
from .serializers import AppointmentSerializer
from .utils import *
from drf_spectacular.utils import extend_schema




# Create your views here.
@extend_schema(tags=['Appointments'])
class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        appointment = serializer.save()
        notify_admin_of_new_appointment(appointment)
        # send_sms_to_admin(appointment) 


