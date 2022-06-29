from django.db import models
from personal_account.models import User


class Category(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(verbose_name='Название', max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Тэг')
    title = models.CharField(verbose_name='Заголовок', max_length=250)
    short_desc = models.CharField(verbose_name='Краткое описание', max_length=500, blank=True)
    body = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='image_article', verbose_name='Фото', blank=True)
    like = models.BigIntegerField(verbose_name='Количество лайков', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_articles')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    is_parent = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_comments')

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.body

    def children(self):
        return Comment.objects.filter(parent=self)

    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    article = models.ForeignKey(Article, models.CASCADE, related_name='+')
    user = models.ForeignKey(User, models.CASCADE)
