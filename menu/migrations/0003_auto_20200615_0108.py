# Generated by Django 3.0.6 on 2020-06-15 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20200615_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='addextra',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='salad',
            name='meal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='salad_meal', to='menu.Meal'),
        ),
    ]
