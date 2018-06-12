import datetime

from django.db import models


class Apiary(models.Model):
    """
    Location where beehives and nucs are kept.
    """
    label = models.CharField(max_length=200, verbose_name='Nombre')
    owner = models.ForeignKey('auth.User', related_name='apiaries', on_delete=models.CASCADE)
    status = models.ForeignKey('ApiaryStatus', on_delete=models.CASCADE,
                               related_name='current', null=True)

    class Meta:
        ordering = ['owner', 'label']

    def __str__(self):
        return self.label


class ApiaryStatus(models.Model):
    apiary = models.ForeignKey(Apiary, on_delete=models.CASCADE, related_name='status_history')
    date = models.DateField(verbose_name='fecha')
    nucs = models.IntegerField(verbose_name='núcleos')
    hives = models.IntegerField(verbose_name='colmenas')

    class Meta:
        ordering = ['-date']


class Harvest(models.Model):
    apiary = models.ForeignKey(Apiary, on_delete=models.CASCADE, related_name='harvest')
    amount = models.IntegerField(verbose_name='cantidad')
    date = models.DateField(verbose_name='fecha')
