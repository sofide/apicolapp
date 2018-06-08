from django.shortcuts import render, redirect, get_object_or_404

from apiary.models import Apiary, ApiaryStatus
from apiary.forms import ApiaryForm


def index(request):
    if request.user.is_authenticated:
        apiaries = ApiaryStatus.objects.select_related('apiary').filter(
            apiary__owner=request.user,
            current=True
        )

    else:
        apiaries = []

    return render(request, 'apiary/index.html', {'apiaries': apiaries})


def edit_apiary(request, apiary_pk=None):
    if apiary_pk:
        apiary_instance = get_object_or_404(Apiary, pk=apiary_pk)
        if apiary_instance.owner != request.user:
            return redirect('apiary_index')
    else:
        apiary_instance = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            apiary_form = ApiaryForm(request.POST, instance=apiary_instance)

            if apiary_form.is_valid():
                new_apiary = apiary_form.save(commit=False)
                new_apiary.owner = request.user
                new_apiary.save()

                return redirect('apiary_index')

        elif apiary_pk:
            apiary = get_object_or_404(Apiary, pk=apiary_pk)
            apiary_form = ApiaryForm(instance=apiary)
        else:
            apiary_form = ApiaryForm()

        return render(request, 'apiary/new_apiary.html', {
            'apiary_form': apiary_form,
            'instance': apiary_instance,
        })
