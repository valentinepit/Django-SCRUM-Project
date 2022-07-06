from datetime import datetime, timedelta

import pytz

from django.utils import timezone
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
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name if self.first_name else self.username

    def as_activate_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activate_key_expired + timedelta(hours=48):
            return True
        return False


class Notification(models.Model):
    # 0 = @moderator, 1 = Like_Article, 2 = Comment, 3 = Like_Comment, 4 = Reply
    AT_MODERATOR = 0
    LIKE_ARTICLE = 1
    COMMENT = 2
    LIKE_COMMENT = 3
    REPLY = 4

    NOTE = (
        (AT_MODERATOR, '@moderator'),
        (LIKE_ARTICLE, 'Like_Article'),
        (COMMENT, 'Comment'),
        (LIKE_COMMENT, 'Like_Comment'),
        (REPLY, 'Reply')
    )
    notification_type = models.IntegerField(choices=NOTE, verbose_name='Тип')
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    object_id = models.IntegerField(verbose_name="id комментария/поста", blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

    def get_article(self):
        from mainapp.models import Article
        return Article.objects.get(id=self.object_id)

    def get_comment(self):
        from mainapp.models import Comment
        return Comment.objects.get(id=self.object_id)

    def __str__(self):
        return str(self.from_user) + ": " + self.get_notification_type_display() + ' ' + str(self.to_user)
