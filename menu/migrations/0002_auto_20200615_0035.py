# Generated by Django 3.0.6 on 2020-06-15 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salad',
            old_name='meal_id',
            new_name='meal',
        ),
    ]
