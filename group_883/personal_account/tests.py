from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from django.contrib.auth.models import Group

from .models import Notification, User
from mainapp.models import Article, Tag, Category, Comment


class TestNotificationSmoke(TestCase):
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

    def test_notification_urls(self):
        note = Notification.objects.create(notification_type=1, to_user=self.superuser,
                                           from_user=self.superuser, object_id=Article.objects.first().id,
                                           user_has_seen=False)
        response = self.client.get(reverse('personal_account:article-notification', kwargs={'notification_pk': note.pk,
                                                                                            'article_pk': note.get_article().id}))
        self.assertEqual(response.status_code, self.status_redirect)

        note.user_has_seen = False
        note.save()

        self.assertEqual(False, Notification.objects.get(id=note.id).user_has_seen)
        response = self.client.delete(
            reverse('personal_account:notification-delete', kwargs={'notification_pk': note.pk, }))
        self.assertEqual(True, Notification.objects.get(id=note.id).user_has_seen)

    def test_notification_signals(self):

        self.newuser = User.objects.create_superuser(
            username=self.newuser,
            password=self.password,
        )

        self.client.login(username=self.newuser, password=self.password)

        article = Article.objects.first()

        new_group = Group.objects.create(name='moderators')
        new_group.user_set.add(self.newuser)

        new_group = Group.objects.create(name='admins')
        new_group.user_set.add(self.superuser)

        comment = Comment.objects.create(
            article=article,
            user=self.superuser,
            body="@moderator",
        )

        self.assertEqual(Notification.objects.filter(object_id=comment.id).last().notification_type, 0)
        self.assertEqual(Notification.objects.filter(object_id=comment.id).count(), 2)

        response = self.client.post(reverse('rating:like_article', kwargs={'pk': article.pk, }),
                                    **{'HTTP_X_REQUESTED_WITH':
                                    'XMLHttpRequest'})

        article = Article.objects.get(pk=article.pk)

        self.assertEqual(Notification.objects.filter(object_id=article.id).last().notification_type, 1)

        comment = Comment.objects.create(
            article=article,
            user=self.newuser,
            body="Text",
        )

        self.assertEqual(Notification.objects.filter(object_id=comment.id).last().notification_type, 2)

        comment = Comment.objects.create(
            article=article,
            user=self.superuser,
            body="Text",
        )

        response = self.client.post(reverse('rating:like_comment', kwargs={'pk': comment.pk, }),
                                    **{'HTTP_X_REQUESTED_WITH':
                                    'XMLHttpRequest'})

        self.assertEqual(Notification.objects.filter(object_id=comment.id).last().notification_type, 3)

        comment = Comment.objects.create(
            article=article,
            user=self.newuser,
            body="Resp",
            is_parent=False,
            parent=comment,
        )

        self.assertEqual(Notification.objects.filter(object_id=comment.id).last().notification_type, 4)

        a = Article.objects.create(
            category=self.category,
            user=self.superuser,
            tag=self.tag,
            title=f'article--1',
            short_desc=f"Short desc-1",
            body=f"Lorem-1",
            moderated=0,
        )

        a.moderated = 1
        a.save()

        self.assertEqual(Notification.objects.filter(object_id=a.id).last().notification_type, 5)
