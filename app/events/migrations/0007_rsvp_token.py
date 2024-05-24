# Generated by Django 5.0.6 on 2024-05-24 18:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_rsvp'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsvp',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
