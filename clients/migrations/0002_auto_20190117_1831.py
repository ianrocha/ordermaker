# Generated by Django 2.1.5 on 2019-01-17 21:31

import clients.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=clients.models.upload_to),
        ),
    ]
