from django import forms
from accounting.models import Product, Purchase, Sale


class ProductForm(forms.ModelForm):
    """Form to create or edit a product."""
    class Meta:
        model = Product
        fields = ['category', 'name', 'description']


class PurchaseForm(forms.ModelForm):
    """Form to create or edit an specific product's purchase."""
    class Meta:
        model = Purchase
        fields = ['amount', 'value', 'date']

        widgets = {'date': forms.DateInput(attrs={'id': 'datepicker_field'})}


class PurchaseDepreciationForm(PurchaseForm):
    """Purchase form with extra fields for depreciation info."""
    model_year = forms.IntegerField(min_value=1900)


class SaleForm(forms.ModelForm):
    """Form to create or edit a sale."""
    class Meta:
        model = Sale
        exclude = ['user', 'logged_datetime']
        widgets = {'date': forms.DateInput(attrs={'id': 'datepicker_field'})}


class DateFromToForm(forms.Form):
    from_date = forms.DateField(label='Desde')
    to_date = forms.DateField(label='Hasta')
