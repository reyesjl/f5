# Generated by Django 5.0.6 on 2024-09-25 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0002_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='goal',
            field=models.CharField(blank=True, choices=[('strength', 'Strength'), ('conditioning', 'Conditioning'), ('speed', 'Speed'), ('endurance', 'Endurance'), ('recovery', 'Recovery')], max_length=50),
        ),
    ]
