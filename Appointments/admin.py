from django.contrib import admin
from .models import Appointment
from django.utils.html import format_html
import datetime
from django.http import HttpResponse
from docx import Document
from docx.shared import Inches
from .models import Appointment
from django.urls import path
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import datetime
from io import BytesIO
from django.http import HttpResponse

# Register your models here.

def mark_as_confirmed(modeladmin, request, queryset):
    for appointment in queryset:
        appointment.status = 'confirmed'
        appointment.save()
mark_as_confirmed.short_description = "Mark selected appointments as Confirmed"

def mark_as_cancelled(modeladmin, request, queryset):
    for appointment in queryset:
        appointment.status = 'cancelled'
        appointment.is_cancelled = True
        appointment.save()
mark_as_cancelled.short_description = "Mark selected appointments as Cancelled"

def mark_as_reschedule(modeladmin, request, queryset):
    for appointment in queryset:
        appointment.status = 'to-be-rescheduled'
        appointment.save()
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'download-confirmed/',
                self.admin_site.admin_view(self.export_todays_confirmed_appointments),
                name='appointments_appointment_download-confirmed'
            ),
        ]
        return custom_urls + urls

    def export_todays_confirmed_appointments(self, request):
        today = datetime.date.today()
        confirmed_appointments = Appointment.objects.filter(
            status='confirmed',
            preferred_date__date=today
        )

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph(f"Confirmed Appointments – {today.strftime('%B %d, %Y')}", styles['Title']))
        elements.append(Spacer(1, 12))

        data = [['S/N', 'Full Name', 'Email', 'Phone', 'Appointment Date']]
        for idx, appointment in enumerate(confirmed_appointments, start=1):
            data.append([
                str(idx),
                appointment.full_name,
                appointment.email,
                appointment.phone,
                appointment.preferred_date.strftime('%B %d, %Y')
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10284e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=confirmed_appointments_{today}.pdf'
        return response

    export_todays_confirmed_appointments.short_description = "Export Today's Confirmed Appointments as PDF"
