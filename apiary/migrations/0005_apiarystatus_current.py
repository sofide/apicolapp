# Generated by Django 2.0.5 on 2018-06-07 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiary', '0004_auto_20180607_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiarystatus',
            name='current',
            field=models.BooleanField(default=False),
        ),
    ]