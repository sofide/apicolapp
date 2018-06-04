from django.forms import ModelForm
from accounting.models import Product, Purchase


class ProductForm(ModelForm):
    '''form to create or edit a product'''
    class Meta:
        model = Product
        fields = ['name', 'description']


class PurchaseForm(ModelForm):
    '''form to create or edit an specific product's purchase'''
    class Meta:
        model = Purchase
        fields = ['amount', 'date']

