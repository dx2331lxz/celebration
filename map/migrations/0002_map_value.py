# Generated by Django 5.0.2 on 2024-04-06 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='value',
            field=models.IntegerField(default=0, verbose_name='value'),
        ),
    ]
