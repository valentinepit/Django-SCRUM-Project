from django.db import models
from personal_account.models import User


class Category(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(verbose_name='Название', max_length=20)

    def __str__(self):
        return self.title


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(verbose_name='Заголовок', max_length=60)
    short_desc = models.CharField(verbose_name='Краткое описание', max_length=500, blank=True)
    body = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='image_article', verbose_name='Фото', blank=True)
    like = models.BigIntegerField(verbose_name='Количество лайков')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    def __str__(self):
        return self.body


class Like(models.Model):
    article = models.ForeignKey(Article, models.CASCADE, related_name='+')
    user = models.ForeignKey(User, models.CASCADE)
