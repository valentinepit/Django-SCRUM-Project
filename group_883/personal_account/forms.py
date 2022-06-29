from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
import hashlib

from personal_account.models import User
from mainapp.models import Article


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'foto', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.activate_key = hashlib.sha1(user.email.encode('utf-8')).hexdigest()
        user.activate_key_expired = datetime.now(pytz.timezone(settings.TIME_ZONE))

        user.save()
        return user


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'foto', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('category', 'tag', 'title', 'short_desc', 'body', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
