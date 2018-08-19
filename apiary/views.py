import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from apiary.models import Apiary, ApiaryStatus, Harvest
from apiary.forms import ApiaryForm, HarvestForm
from apiary.data import apiary_history_table, apiary_history_chart


@login_required
def index(request):
    if request.user.is_authenticated:
        apiaries = Apiary.objects.select_related('status').filter(owner=request.user)

    else:
        apiaries = []

    return render(request, 'apiary/index.html', {'apiaries': apiaries})


def apiary_abm(request, apiary_pk=None):
    if apiary_pk:
        apiary_instance = get_object_or_404(Apiary, pk=apiary_pk)
        if apiary_instance.owner != request.user:
            return HttpResponseForbidden()
        apiary_data = {
            'label': apiary_instance.label,
            'nucs': apiary_instance.status.nucs,
            'hives': apiary_instance.status.hives,
            'date': datetime.datetime.today(),
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


def apiary_detail(request, apiary_pk):
    apiary = get_object_or_404(Apiary, pk=apiary_pk)
    if apiary.owner != request.user:
        return HttpResponseForbidden()

    history_table = apiary_history_table(apiary)
    script, div = apiary_history_chart(history_table['body'], apiary.label)

    return render(request, 'apiary/detail.html', {
        'apiary': apiary,
        'history_table': history_table,
        'div': div,
        'script': script,
    })


def harvest_list(request):
    harvests = Harvest.objects.filter(apiary__owner=request.user)

    return render(request, 'apiary/harvest_list.html', {'harvests':harvests})


def harvest(request, harvest_pk=None):
    if harvest_pk:
        harvest_instance = get_object_or_404(Harvest, pk=harvest_pk)
        if harvest_instance.apiary.owner != request.user:
            return HttpResponseForbidden()
    else:
        harvest_instance = None

    if request.method == 'POST':
        form = HarvestForm(request.POST, instance=harvest_instance)

        if form.is_valid():
            harvest = form.save()

            return redirect('harvest_list')
    else:
        form = HarvestForm(instance=harvest_instance)

    form.fields['apiary'].queryset = Apiary.objects.filter(owner=request.user)
    return render(request, 'apiary/harvest.html', {
        'form': form, 'instance':harvest_instance
    })
