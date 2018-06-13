from django.shortcuts import render, redirect, get_object_or_404

from apiary.models import Apiary, ApiaryStatus
from apiary.forms import ApiaryForm


def index(request):
    if request.user.is_authenticated:
        apiaries = Apiary.objects.select_related('status').filter(owner=request.user)

    else:
        apiaries = []

    return render(request, 'apiary/index.html', {'apiaries': apiaries})


def edit_apiary(request, apiary_pk=None):
    if apiary_pk:
        apiary_instance = get_object_or_404(Apiary, pk=apiary_pk)
        if apiary_instance.owner != request.user:
            return redirect('apiary_index')
        apiary_data = {
            'label': apiary_instance.label,
            'nucs': apiary_instance.status.nucs,
            'hives': apiary_instance.status.hives,
        }
    else:
        apiary_instance = None
        apiary_data = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            apiary_form = ApiaryForm(request.POST)

            if apiary_form.is_valid():
                label = apiary_form.cleaned_data['label']
                hives = apiary_form.cleaned_data['hives']
                nucs = apiary_form.cleaned_data['nucs']
                date = apiary_form.cleaned_data['date']

                if not apiary_instance:
                    apiary_instance = Apiary.objects.create(label=label, owner=request.user)
                else:
                    apiary_instance.label = label

                status_apiary, created = ApiaryStatus.objects.update_or_create(
                    apiary=apiary_instance,
                    date=date,
                    defaults= {
                        'nucs':nucs,
                        'hives':hives
                    }
                )

                apiary_instance.status = status_apiary
                apiary_instance.save()

                return redirect('apiary_index')

        elif apiary_data:
            apiary_form = ApiaryForm(apiary_data)

        else:
            apiary_form = ApiaryForm()

        return render(request, 'apiary/new_apiary.html', {
            'apiary_form': apiary_form,
            'instance': apiary_instance,
        })
    else:
        return redirect('login')
