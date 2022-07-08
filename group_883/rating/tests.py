from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from personal_account.models import Notification, User
from mainapp.models import Article, Tag, Category, Comment


class TestLikesSmoke(TestCase):
    status_ok = 200
    status_redirect = 302
    username = 'admin'
    password = '1234'
    newuser = 'newuser'

    def setUp(self) -> None:
        self.category = Category.objects.create(
            title='cat1'
        )
        self.tag = Tag.objects.create(
            title='tag1'
        )
        self.superuser = User.objects.create_superuser(
            username=self.username,
            password=self.password,
        )
        for i in range(3):
            Article.objects.create(
                category=self.category,
                user=self.superuser,
                tag=self.tag,
                title=f'article-{i}',
                short_desc=f"Short desc{i}",
                body=f"Lorem{i}",
                moderated=1,
            )

        self.client = Client()

    def test_like(self):

        self.client.login(username=self.username, password=self.password)
        article = Article.objects.first()
        response = self.client.post(reverse('rating:like_article', kwargs={'pk': article.pk, }),
                                    **{'HTTP_X_REQUESTED_WITH':
                                           'XMLHttpRequest'})

        article = Article.objects.get(pk=article.pk)

        self.assertEqual(article.total_likes, 1)
        self.assertEqual(article.user.total_likes, 1)

        response = self.client.post(reverse('rating:like_article', kwargs={'pk': article.pk, }),
                                    **{'HTTP_X_REQUESTED_WITH':
                                           'XMLHttpRequest'})

        article = Article.objects.get(pk=article.pk)
        self.assertEqual(article.total_likes, 0)
        self.assertEqual(article.user.total_likes, 0)

    def test_comment_like(self):
        self.client.login(username=self.username, password=self.password)
        article = Article.objects.first()
        comment = Comment.objects.create(
            article=article,
            user=self.superuser,
            body="Text",
        )
        response = self.client.post(reverse('rating:like_comment', kwargs={'pk': comment.pk, }),
                                    **{'HTTP_X_REQUESTED_WITH':
                                           'XMLHttpRequest'})

        comment = Comment.objects.get(pk=comment.pk)

        self.assertEqual(comment.total_likes(), 1)
        self.assertEqual(comment.user.total_likes, 0)

        response = self.client.post(reverse('rating:like_comment', kwargs={'pk': comment.pk, }),
                                    **{'HTTP_X_REQUESTED_WITH':
                                           'XMLHttpRequest'})

        comment = Comment.objects.get(pk=comment.pk)
        self.assertEqual(comment.total_likes(), 0)
        self.assertEqual(comment.user.total_likes, 0)
