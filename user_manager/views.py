from django.shortcuts import render, redirect
from django.contrib import auth

from user_manager import forms


def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')

        error_message = ('Usuario o contraseña no válidos')

        return render(request, 'user_manager/login.html', {
            'error_message': error_message,
            'login_form': login_form,
        })

    else:
        login_form = forms.LoginForm()
        return render(request, 'user_manager/login.html', {'login_form': login_form})


def logout(request):
    auth.logout(request)
    return redirect('/')
