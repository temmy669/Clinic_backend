from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        
    def validate(self, attrs):
        preferred_date = attrs.get('preferred_date')
        preferred_time = attrs.get('preferred_time')

        # Check if there's already a confirmed or pending appointment at that date & time
        if Appointment.objects.filter(
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            is_cancelled=False,
            status__in=['pending', 'confirmed']
        ).exists():
            raise serializers.ValidationError(
                "This time slot has already been booked by another patient. Please choose a different time."
            )
        return attrs    
    
