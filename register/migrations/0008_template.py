# Generated by Django 5.0.1 on 2024-09-11 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0007_userresumedetails_created_at_userresumedetails_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.TextField()),
            ],
        ),
    ]