# Generated by Django 4.1.7 on 2023-03-04 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to=''),
        ),
    ]
