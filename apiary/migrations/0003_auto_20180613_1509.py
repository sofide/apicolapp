# Generated by Django 2.0.5 on 2018-06-13 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiary', '0002_auto_20180613_1501'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='apiarystatus',
            unique_together={('apiary', 'date')},
        ),
    ]
