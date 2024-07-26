# Generated by Django 5.0.6 on 2024-07-26 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0011_plan_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='movement',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='content',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='reading_time',
        ),
        migrations.DeleteModel(
            name='Movement',
        ),
        migrations.DeleteModel(
            name='Exercise',
        ),
        migrations.DeleteModel(
            name='Meal',
        ),
    ]