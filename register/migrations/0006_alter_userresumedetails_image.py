# Generated by Django 5.0.1 on 2024-09-11 14:06

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_alter_userresumedetails_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresumedetails',
            name='image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(), upload_to='images/'),
        ),
    ]
