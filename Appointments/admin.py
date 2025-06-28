from django.contrib import admin
from .models import Appointment
from django.utils.html import format_html

# Register your models here.

def mark_as_confirmed(modeladmin, request, queryset):
    queryset.update(status='confirmed')
mark_as_confirmed.short_description = "Mark selected appointments as Confirmed"

def mark_as_cancelled(modeladmin, request, queryset):
    queryset.update(status='cancelled')
mark_as_cancelled.short_description = "Mark selected appointments as Cancelled"

def mark_as_reschedule(modeladmin, request, queryset):
    queryset.update(status='to-be-rescheduled')
mark_as_reschedule.short_description = "Mark selected appointments as To-be-rescheduled"



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'preferred_date', 'status', 'created_at',)
    list_filter = ('status', 'preferred_date')
    search_fields = ('full_name', 'email', 'phone')
    ordering = ('-created_at',)

    list_editable = ('status',)

    actions = [mark_as_confirmed, mark_as_cancelled, mark_as_reschedule]

    class Media:
        css = {
            'all': ('appointments/css/admin_status_colors.css',),
        }
        js = ('appointments/js/admin_status_colors.js',)