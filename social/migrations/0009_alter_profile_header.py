# Generated by Django 4.1.7 on 2023-03-08 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_remove_profile_display_name_profile_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='header',
            field=models.ImageField(default='default_header.png', upload_to='header_pics'),
        ),
    ]
