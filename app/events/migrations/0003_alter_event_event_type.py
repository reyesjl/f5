# Generated by Django 5.0.6 on 2024-05-24 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_event_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('camp', 'Camp'), ('game', 'Game'), ('training', 'Training'), ('clinic', 'Clinic'), ('combine', 'Combine'), ('other', 'Other')], max_length=50),
        ),
    ]
