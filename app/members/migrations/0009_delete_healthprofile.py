# Generated by Django 5.0.6 on 2024-07-12 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_alter_customuser_is_trainer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HealthProfile',
        ),
    ]
