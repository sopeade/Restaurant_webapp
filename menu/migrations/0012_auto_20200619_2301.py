# Generated by Django 3.0.6 on 2020-06-20 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0011_auto_20200619_2130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='orders',
            new_name='order',
        ),
    ]