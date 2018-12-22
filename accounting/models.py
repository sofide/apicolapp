from django.db import models


class Category(models.Model):
    """
    Category of products, for example: vehicle, supply, etc.
    """
    label = models.CharField(max_length=200)
    description = models.TextField()
    depreciation_period = models.IntegerField()

    class Meta:
        ordering = ['label',]

    def __str__(self):
        return self.label


class Product(models.Model):
    """
    User products that are used in the beekeeping activities.
    """
    name = models.CharField(max_length=200, verbose_name='nombre')
    description = models.TextField(verbose_name='descripción')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name='categoría')

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Purchase(models.Model):
    """
    Product's purchases to track expenses.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases',
                                verbose_name='producto')
    date = models.DateField(verbose_name='fecha')
    amount = models.FloatField(verbose_name='cantidad')
    value = models.FloatField(verbose_name='monto pagado')
    logged_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'product']

    def __str__(self):
        return '{} - {}'.format(self.date, self.product)


class DepreciationInfo(models.Model):
    """
    'Purchase' extra info, to calculate depreciation of products
    that are in categories with depreciation_period.
    """
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    model_year = models.IntegerField()

    class Meta:
        ordering = ['purchase']

    def __str__(self):
        return '{} - {}'.format(self.purchase.product, self.model_year)
