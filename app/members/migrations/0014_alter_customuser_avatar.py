# Generated by Django 5.0.6 on 2024-07-31 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/avatars/'),
        ),
    ]
