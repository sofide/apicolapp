from django.forms import ModelForm, IntegerField, DateField, DateInput
from accounting.models import Product, Purchase, Sale


class ProductForm(ModelForm):
    """Form to create or edit a product."""
    class Meta:
        model = Product
        fields = ['category', 'name', 'description']


class PurchaseForm(ModelForm):
    """Form to create or edit an specific product's purchase."""
    class Meta:
        model = Purchase
        fields = ['amount', 'value', 'date']

        widgets = {'date': DateInput(attrs={'id': 'purchase_datepicker'})}


class PurchaseDepreciationForm(PurchaseForm):
    """Purchase form with extra fields for depreciation info."""
    model_year = IntegerField(min_value=1900)


class SaleForm(ModelForm):
    """Form to create or edit a sale."""
    class Meta:
        model = Sale
        exclude = ['user', 'logged_datetime']
