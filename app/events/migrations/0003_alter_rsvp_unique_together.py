# Generated by Django 5.0.6 on 2024-06-03 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_rsvp_slug'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rsvp',
            unique_together=set(),
        ),
    ]