# Generated by Django 2.0.5 on 2018-06-13 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiary', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='harvest',
            options={'ordering': ['-date']},
        ),
    ]
