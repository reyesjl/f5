# Generated by Django 5.0.6 on 2024-05-28 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsvp',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]