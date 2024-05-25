# Generated by Django 5.0.6 on 2024-05-24 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_detailed_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rsvp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('role', models.CharField(choices=[('player', 'Player'), ('coach', 'Coach'), ('spectator', 'Spectator')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rsvps', to='events.event')),
            ],
            options={
                'unique_together': {('event', 'email')},
            },
        ),
    ]