# Generated by Django 5.0.2 on 2024-04-06 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_map_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='value',
            field=models.IntegerField(default=1, verbose_name='value'),
        ),
    ]
