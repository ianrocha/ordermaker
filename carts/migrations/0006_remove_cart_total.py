# Generated by Django 2.1.5 on 2019-01-24 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_auto_20190122_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total',
        ),
    ]
