from datetime import datetime

from django import forms
from apiary.models import Apiary


class ApiaryForm(forms.Form):
    label = forms.CharField(max_length=200, label='Nombre del apiario')
    hives = forms.IntegerField(label='Cantidad de colmenas')
    nucs = forms.IntegerField(label='Cantidad de núcleos')
    date = forms.DateField(initial=datetime.today())
