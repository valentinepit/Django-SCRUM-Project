from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView, View

from group_883.settings import BASE_URL
from personal_account.forms import UserLoginForm, UserRegisterForm, UserEditForm, CreateArticleForm
from mainapp.models import Article
from .models import User, Notification
from mainapp.views import get_popular_tags


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
    if request.method == 'POST' and request.user.is_active == False:
        return render(request, 'personal_account/is_blocked.html')

    context = {
        'login_form': login_form,
        'next_param': next_param,
        'popular_tags': get_popular_tags(),
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
            return HttpResponseRedirect(reverse('mainapp:index'))
    else:
        register_form = UserRegisterForm()
    context = {
        'register_form': register_form,
        'popular_tags': get_popular_tags(),
    }
    return render(request, 'personal_account/register.html', context)


@login_required()
def edit(request, pk):
    current_user = User.objects.get(pk=pk)
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=current_user)
        if (request.user.has_perm('personal_account.change_user') and request.user.groups.filter(
                name='admins') and edit_form.is_valid() or (current_user == request.user and edit_form.is_valid())):
            edit_form.save()
            return redirect('personal_account:our_user', pk=current_user.pk)
    else:
        edit_form = UserEditForm(instance=current_user)
    context = {
        'edit_form': edit_form,
        'current_user': User.objects.get(pk=pk),
        'popular_tags': get_popular_tags(),

    }
    return render(request, 'personal_account/edit.html', context)


@login_required()
def user(request):
    context = {
        'popular_tags': get_popular_tags(),
    }
    return render(request, 'personal_account/user.html', context)


class UserDetail(DetailView):
    model = User
    template_name = 'personal_account/our_account.html'
    context_object_name = 'current_user'

    def get_context_data(self, **kwargs):
        if kwargs["object"].is_private:
            self.privat_account(kwargs["object"])
        context = super(UserDetail, self).get_context_data(**kwargs)
        context.update({
            'popular_tags': get_popular_tags(),
        })
        return context

    def privat_account(self, _user):
        print(f"{_user.is_private=}")
        return HttpResponseRedirect(reverse('personal_account:privat_account'))


def privat_account(request):
    print("HELLO")
    return render(request, 'personal_account/privat_account.html')


class ListArticle(ListView):
    model = Article
    template_name = 'personal_account/article_list.html'
    paginate_by = 2

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).order_by('-is_active')

    def get_context_data(self, **kwargs):
        context = super(ListArticle, self).get_context_data(**kwargs)
        context.update({
            'popular_tags': get_popular_tags(),
        })
        return context


class CreateArticle(CreateView):
    model = Article
    template_name = 'personal_account/article_create.html'
    form_class = CreateArticleForm

    def get_success_url(self):
        return reverse('personal_account:list_article')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateArticle, self).get_context_data(**kwargs)
        context.update({
            'popular_tags': get_popular_tags(),
        })
        return context


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

    def get_context_data(self, **kwargs):
        context = super(EditArticle, self).get_context_data(**kwargs)
        context.update({
            'popular_tags': get_popular_tags(),
        })
        return context

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

    def get_context_data(self, **kwargs):
        context = super(DeleteArticle, self).get_context_data(**kwargs)
        context.update({
            'popular_tags': get_popular_tags(),
        })
        return context


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


def create_permissions(request, pk):
    if request.user.groups.filter(name='admins') and request.user.has_perm('personal_account.change_user'):
        current_user = User.objects.filter(pk=pk).first()
        moders_group = Group.objects.filter(name='moderators').first()
        current_user.groups.add(moders_group)
    return render(request, 'personal_account/is_moder.html')


def delete_permissions(request, pk):
    if request.user.groups.filter(name='admins') and request.user.has_perm('personal_account.change_user'):
        current_user = User.objects.filter(pk=pk).first()
        moders_group = Group.objects.filter(name='moderators').first()
        moders_group.user_set.remove(current_user)
    return render(request, 'personal_account/delete_moder.html')


def delete_user(request, pk):
    user = User.objects.filter(pk=pk).first()
    if request.user.has_perm('personal_account.delete_user') and request.user.groups.filter(name='admins'):
        u = User.objects.get(username=user.username)
        u.delete()
    return render(request, 'personal_account/user_delete.html')


class PostNotification(View):
    def get(self, request, notification_pk, article_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        # article = Article.objects.get(pk=article_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('mainapp:article', pk=article_pk)


def block_render(request, pk):
    blocked_user = User.objects.get(pk=pk)
    context = {
        'blocked_user': blocked_user,
    }
    return render(request, 'personal_account/block.html', context)


def blocked(request, pk):
    user_blocked = User.objects.get(pk=pk)
    context = {
        'blocked_user': user_blocked,
    }
    if (user_blocked and user_blocked.is_active and request.user.groups.filter(
            name='admins')) or (
            user_blocked and user_blocked.is_active and request.user.groups.filter(name='moderators')):
        user_blocked.is_active = False
        user_blocked.save()
        [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user_blocked.id]
        return render(request, 'personal_account/block.html', context)
    elif (user_blocked and user_blocked.is_active == False and request.user.groups.filter(
            name='admins')) or (
            user_blocked and user_blocked.is_active == False and request.user.groups.filter(name='moderators')):
        user_blocked.is_active = True
        user_blocked.save()
        return render(request, 'personal_account/block.html', context)


class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = User.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', pk=profile_pk)


class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')


class PasswordChange(PasswordChangeView):
    def get_context_data(self, **kwargs):
        context = super(PasswordChange, self).get_context_data(**kwargs)
        context.update({
            'popular_tags': get_popular_tags(),
        })
        return context


def change_privat_status(request, pk):
    _user = User.objects.get(pk=pk)
    _user.is_private = False if _user.is_private is True else True
    _user.save()
    return redirect('personal_account:user')
