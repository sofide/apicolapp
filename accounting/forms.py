from django.forms import ModelForm
from accounting.models import Product, Purchase, Sale


class ProductForm(ModelForm):
    '''form to create or edit a product'''
    class Meta:
        model = Product
        fields = ['category', 'name', 'description']


class PurchaseForm(ModelForm):
    '''form to create or edit an specific product's purchase'''
    class Meta:
        model = Purchase
        fields = ['amount', 'value', 'date']


class SaleForm(ModelForm):
    '''form to create or edit a sale'''
    class Meta:
        model = Sale
        exclude = ['user', 'logged_datetime']
