# Generated by Django 5.0.6 on 2024-07-22 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0007_alter_healthprofile_bronco'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='content',
        ),
        migrations.AddField(
            model_name='plan',
            name='exercises',
            field=models.ManyToManyField(related_name='plans', to='health.exercise'),
        ),
    ]
