# Generated by Django 2.1.5 on 2019-01-25 19:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_total'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 1, 25, 19, 45, 52, 820603, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
