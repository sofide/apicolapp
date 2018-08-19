from datetime import datetime

from django import forms
from apiary.models import Apiary, Harvest


class ApiaryForm(forms.Form):
    label = forms.CharField(max_length=200, label='Nombre del apiario')
    hives = forms.IntegerField(label='Cantidad de colmenas')
    nucs = forms.IntegerField(label='Cantidad de núcleos')
    date = forms.DateField(initial=datetime.today(), label='Fecha')


class HarvestForm(forms.ModelForm):
    class Meta:
        model = Harvest
        fields = {
            'apiary': 'Apiario',
            'amount': 'Cantidad cosechada',
            'date': 'fecha'
        }
