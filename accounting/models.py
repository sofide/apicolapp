from django.db import models


class Product(models.Model):
    '''location where beehives and nucs are kept'''
    name = models.CharField(null=True, max_length=200, blank=True, verbose_name='Nombre')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Purchase(models.Model):
    '''purchase of a single product'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    user = models.ForeignKey('auth.User', related_name='purchases', on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Cantidad')
    date = models.DateField(verbose_name='Fecha')

    class Meta:
        ordering = ['date', 'product']


class Inventary(models.Model):
    '''date in which all products in stock are counted'''
    user = models.ForeignKey('auth.User', related_name='inventaries', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Fecha')

    class Meta:
        ordering = ['date']


class InventaryProduct(models.Model):
    '''product counted in an inventary'''
    inventary = models.ForeignKey(Inventary, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Cantidad')

    class Meta:
        ordering = ['inventary', 'product']
