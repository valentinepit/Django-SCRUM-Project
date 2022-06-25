from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    foto = models.ImageField(upload_to='user_foto', verbose_name='Фото', blank=True, default='user_foto/default.jpg')
    description = models.TextField(verbose_name='О себе', blank=True)
    is_admin = models.BooleanField(default=False)
    is_moder = models.BooleanField(default=False)
    birthday = models.DateField(verbose_name='День рождения', null=True)
    total_likes = models.IntegerField(verbose_name='Кол-во лайков автора', default=0)
    email = models.EmailField(("email address"), blank=True)
    activate_key = models.CharField(max_length=128, verbose_name='Ключ активации', blank=True, null=True)
    activate_key_expired = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.first_name

    def as_activate_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activate_key_expired + timedelta(hours=48):
            return True
        return False
