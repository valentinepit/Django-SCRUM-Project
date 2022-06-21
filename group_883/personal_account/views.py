from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from personal_account.forms import UserLoginForm, UserRegisterForm, UserEditForm, CreateArticleForm
from mainapp.models import Article


def login(request):
    login_form = UserLoginForm(data=request.POST)

    next_param = request.GET.get('next', '')

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('mainapp:index'))

    context = {
        'login_form': login_form,
        'next_param': next_param,
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


@login_required()
def edit(request):
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('personal_account:user'))
    else:
        edit_form = UserEditForm(instance=request.user)
    context = {
        'edit_form': edit_form
    }
    return render(request, 'personal_account/edit.html', context)


@login_required()
def user(request):
    return render(request, 'personal_account/user.html')


class ListArticle(ListView):
    model = Article
    template_name = 'personal_account/article_list.html'

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)


class CreateArticle(CreateView):
    model = Article
    template_name = 'personal_account/article_create.html'
    form_class = CreateArticleForm

    def get_success_url(self):
        return reverse('personal_account:list_article')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditArticle(UpdateView):
    model = Article
    template_name = 'personal_account/article_edit.html'
    form_class = CreateArticleForm

    def get_success_url(self):
        return reverse('personal_account:list_article')


class DeleteArticle(DeleteView):
    model = Article
    template_name = 'personal_account/article_delete.html'

    def get_success_url(self):
        return reverse('personal_account:list_article')


def password_change_done(request):
    logout(request)
    return redirect('personal_account:login')
