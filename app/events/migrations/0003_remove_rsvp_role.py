# Generated by Django 5.0.6 on 2024-06-24 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_event_cost_remove_event_cost_secondary_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rsvp',
            name='role',
        ),
    ]
