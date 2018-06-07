from django.db import models


class Apiary(models.Model):
    '''location where beehives and nucs are kept'''
    label = models.CharField(max_length=200, verbose_name='Nombre')
    owner = models.ForeignKey('auth.User', related_name='apiaries', on_delete=models.CASCADE)

    def __str__(self):
        return self.label


class ApiaryStatus(models.Model):
    apiary = models.ForeignKey(Apiary, on_delete=models.CASCADE, related_name='status')
    date = models.DateField(verbose_name='fecha')
    nucs = models.IntegerField(verbose_name='núcleos')
    hives = models.IntegerField(verbose_name='colmenas')
    current = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        '''it shouldn't save two current status for the same apiary'''
        if self.current:
            try:
                old_current = ApiaryStatus.objects.get(apiary=self.apiary, current=True)
                if self != old_current:
                    old_current.current = False
                    old_current.save()
            except ApiaryStatus.DoesNotExist:
                pass

        super(ApiaryStatus, self).save(*args, **kwargs)


class Harvest(models.Model):
    apiary = models.ForeignKey(Apiary, on_delete=models.CASCADE, related_name='harvest')
    amount = models.IntegerField(verbose_name='cantidad')
    date = models.DateField(verbose_name='fecha')
