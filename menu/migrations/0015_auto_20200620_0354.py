# Generated by Django 3.0.6 on 2020-06-20 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0014_auto_20200620_0346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_username',
            new_name='username',
        ),
    ]
