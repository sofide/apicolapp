from django.db import models


class Apiary(models.Model):
    '''location where beehives and nucs are kept'''
    hive = models.IntegerField(default=0, verbose_name='Colmenas')
    nuc = models.IntegerField(default=0, verbose_name='Núcleos')
    label = models.CharField(max_length=200, verbose_name='Nombre')
    owner = models.ForeignKey('auth.User', related_name='apiaries', on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - {} nuc - {} hive".format(self.label, self.owner, self.nuc, self.hive)
