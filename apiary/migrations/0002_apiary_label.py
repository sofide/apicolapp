# Generated by Django 2.0.5 on 2018-05-29 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiary',
            name='label',
            field=models.CharField(default='apiario', max_length=200),
            preserve_default=False,
        ),
    ]
