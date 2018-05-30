from django.shortcuts import render

from apiary.models import Apiary


def index(request):
    if request.user.is_authenticated:
        apiaries = Apiary.objects.filter(owner=request.user)

    else:
        apiaries = []

    return render(request, 'apiary/index.html', {'apiaries': apiaries})
