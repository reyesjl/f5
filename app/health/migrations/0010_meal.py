# Generated by Django 5.0.6 on 2024-07-23 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0009_remove_plan_exercises_exercise_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='health/meal_images/')),
                ('description', models.TextField()),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='health.plan')),
            ],
        ),
    ]
