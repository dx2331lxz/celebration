# Generated by Django 5.0.2 on 2024-04-09 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='description',
            field=models.TextField(default=1, verbose_name='描述'),
            preserve_default=False,
        ),
    ]
