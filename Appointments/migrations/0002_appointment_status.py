# Generated by Django 5.2.3 on 2025-06-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
