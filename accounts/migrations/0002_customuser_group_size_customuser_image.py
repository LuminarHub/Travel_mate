# Generated by Django 5.1.7 on 2025-03-12 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='group_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='profile_image'),
        ),
    ]
