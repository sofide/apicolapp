from django.forms import ModelForm
from apiary.models import Apiary


class ApiaryForm(ModelForm):
    class Meta:
        model = Apiary
        fields = ['label']
