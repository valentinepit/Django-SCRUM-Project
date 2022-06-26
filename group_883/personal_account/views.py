from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django.contrib.auth import login as log_user

from group_883.settings import BASE_URL
from personal_account.forms import UserLoginForm, UserRegisterForm, UserEditForm, CreateArticleForm
from mainapp.models import Article
from .models import User


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
            new_user = register_form.save()
            send_verify_email(new_user)
            # email = register_form.cleaned_data
            return HttpResponseRedirect(reverse('mainapp:index'))
    else:
        print('asdasd')
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


class UserDetail(DetailView):
    model = User
    template_name = 'personal_account/our_account.html'
    context_object_name = 'current_user'


class ListArticle(ListView):
    model = Article
    template_name = 'personal_account/article_list.html'
    paginate_by = 2

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).filter(is_active=True)


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

    def has_permissions(self, user):
        if user.groups.filter(name='admins') or user.groups.filter(name='moderators') or user.groups.filter(
                name='test_group'):
            return True

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.has_permissions(self.request.user) and obj.user != self.request.user:
            return redirect('personal_account:list_article')
        elif self.request.user.has_perm('mainapp.change_article') or obj.user == self.request.user:
            return super(EditArticle, self).dispatch(request, *args, **kwargs)


class DeleteArticle(DeleteView):
    model = Article
    template_name = 'personal_account/article_delete.html'

    def has_permissions(self, user):
        if user.groups.filter(name='admins') or user.groups.filter(name='moderators'):
            return True

    def get_success_url(self):
        return reverse('personal_account:list_article')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.has_permissions(self.request.user) and obj.user != self.request.user:
            return redirect('personal_account:list_article')
        elif self.request.user.has_perm('mainapp.delete_article') or obj.user == self.request.user:
            return super(DeleteArticle, self).dispatch(request, *args, **kwargs)


def password_change_done(request):
    logout(request)
    return redirect('personal_account:login')


def verify(request, email, key):
    user = User.objects.filter(email=email).first()
    if user:
        if user.activate_key == key and not user.as_activate_key_expired():
            user.is_active = True
            user.activate_key = None
            user.activate_key_expired = None
            user.save()
            auth.login(request, user, backend='django.core.mail.backends.smtp.EmailBackend')
    return render(request, 'personal_account/register_failed.html')


def send_verify_email(user):
    verify_link = reverse('personal_account:verify', args=[user.email, user.activate_key])
    full_link = f'{BASE_URL}{verify_link}'

    message = f'Перейдите по ссылке активации: {full_link}'
    return send_mail(
        'активация аккаунта',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )
