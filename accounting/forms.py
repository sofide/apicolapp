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

        widgets = {'date': forms.DateInput(attrs={'id': 'purchase_datepicker'})}


class PurchaseDepreciationForm(PurchaseForm):
    """Purchase form with extra fields for depreciation info."""
    model_year = forms.IntegerField(min_value=1900)


class SaleForm(forms.ModelForm):
    """Form to create or edit a sale."""
    class Meta:
        model = Sale
        exclude = ['user', 'logged_datetime']


class DateFromToForm(forms.Form):
    from_date = forms.DateField(label='Desde')
    to_date = forms.DateField(label='Hasta')

    class Meta:
        widgets = {'from_date': forms.DateInput(attrs={'id': 'from_datepicker'})}
        widgets = {'to_date': forms.DateInput(attrs={'id': 'to_datepicker'})}

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if from_date < to_date:
            forms.ValidationError('La fecha "hasta" no puede ser menor a la fecha "desde".')
