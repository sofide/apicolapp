from django.db import models


class Apiary(models.Model):
    '''location where beehives and nucs are kept'''
    hive = models.IntegerField(default=0)
    nuc = models.IntegerField(default=0)
    owner = models.ForeignKey('auth.User', related_name='apiaries', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} nuc - {} hive'
