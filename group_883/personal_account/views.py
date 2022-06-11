from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse

from personal_account.forms import UserLoginForm, UserRegisterForm, UserEditForm


def login(request):
    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('mainapp:index'))

    context = {
        'login_form': login_form
    }

    return render(request, 'personal_account/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('mainapp:index'))


def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('mainapp:index'))
    else:
        register_form = UserRegisterForm()
    context = {
        'register_form': register_form
    }
    return render(request, 'personal_account/register.html', context)


def edit(request):
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('personal_account:edit'))
    else:
        edit_form = UserEditForm(instance=request.user)
    context = {
        'edit_form': edit_form
    }
    return render(request, 'personal_account/edit.html', context)
