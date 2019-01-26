from datetime import datetime

from django import forms
from apiary.models import Apiary, Harvest


class ApiaryForm(forms.Form):
    label = forms.CharField(max_length=200, label='Nombre del apiario')
    hives = forms.IntegerField(label='Cantidad de colmenas')
    nucs = forms.IntegerField(label='Cantidad de núcleos')
    date = forms.DateField(
        initial=datetime.today(),
        label='Fecha',
        widget= forms.DateInput(attrs={'id': 'datepicker_field'})
    )


class HarvestForm(forms.ModelForm):
    class Meta:
        model = Harvest
        fields = '__all__'
        labels = {
            'apiary': 'Apiario',
            'amount': 'Cantidad cosechada',
            'date': 'Fecha'
        }
        widgets = {'date': forms.DateInput(attrs={'id': 'datepicker_field'})}
