# Generated by Django 5.0.1 on 2024-09-11 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_alter_userresumedetails_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresumedetails',
            name='certification',
            field=models.ManyToManyField(to='register.certification'),
        ),
        migrations.AlterField(
            model_name='userresumedetails',
            name='experience',
            field=models.ManyToManyField(to='register.experience'),
        ),
        migrations.AlterField(
            model_name='userresumedetails',
            name='image',
            field=models.ImageField(upload_to='media/images/'),
        ),
        migrations.AlterField(
            model_name='userresumedetails',
            name='miniproject',
            field=models.ManyToManyField(to='register.miniprojects'),
        ),
        migrations.AlterField(
            model_name='userresumedetails',
            name='project',
            field=models.ManyToManyField(to='register.project'),
        ),
        migrations.AlterField(
            model_name='userresumedetails',
            name='strength',
            field=models.ManyToManyField(to='register.strength'),
        ),
    ]