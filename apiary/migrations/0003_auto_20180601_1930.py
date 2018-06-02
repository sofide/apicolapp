# Generated by Django 2.0.5 on 2018-06-01 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiary', '0002_apiary_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiary',
            name='hive',
            field=models.IntegerField(default=0, verbose_name='Colmenas'),
        ),
        migrations.AlterField(
            model_name='apiary',
            name='label',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='apiary',
            name='nuc',
            field=models.IntegerField(default=0, verbose_name='Núcleos'),
        ),
    ]