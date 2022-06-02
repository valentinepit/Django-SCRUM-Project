from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    foto = models.ImageField(upload_to='user_foto', verbose_name='Фото', blank=True)
    description = models.TextField(verbose_name='О себе', blank=True)
    is_admin = models.BooleanField(default=False)
    is_moder = models.BooleanField(default=False)
    birthday = models.DateField(verbose_name='День рождения', null=True)

    def __str__(self):
        return self.first_name
