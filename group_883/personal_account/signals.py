from .models import Notification
from mainapp.models import Comment, Article
from personal_account.models import User

from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.db.models import Q


@receiver(post_save, sender=Comment)
def create_comment(sender, instance, created, **kwargs):
    if created:
        if instance.body.startswith('@moderator'):
            moderators = User.objects.filter(Q(groups__name='admins') | Q(groups__name='moderators'))

            for moderator in moderators:
                Notification.objects.get_or_create(notification_type=0, to_user=moderator, from_user=instance.user,
                                                   object_id=instance.article.id, user_has_seen=False)
        else:
            if instance.is_parent and instance.article.user != instance.user:
                Notification.objects.get_or_create(notification_type=2, to_user=instance.article.user,
                                                   from_user=instance.user, object_id=instance.id, user_has_seen=False)
            elif instance.parent.user != instance.user:
                Notification.objects.get_or_create(notification_type=4, to_user=instance.parent.user,
                                                   from_user=instance.user, object_id=instance.id, user_has_seen=False)


@receiver(m2m_changed, sender=Comment.likes.through)
def update_comment(sender, instance, action, pk_set=None, **kwargs):
    if action == 'pre_add':
        for pk in pk_set:
            u = User.objects.get(id=pk)
            if u != instance.user:
                Notification.objects.get_or_create(notification_type=3, to_user=instance.user,
                                                   from_user=u, object_id=instance.id, user_has_seen=False)


@receiver(m2m_changed, sender=Article.likes.through)
def update_article(sender, instance, action, pk_set=None, **kwargs):
    if action == 'pre_add':
        for pk in pk_set:
            u = User.objects.get(id=pk)
            if u != instance.user:
                Notification.objects.get_or_create(notification_type=1, to_user=instance.user,
                                                   from_user=u, object_id=instance.id, user_has_seen=False)


@receiver(pre_save, sender=Article)
def update_article_moderated(sender, instance: Article, **kwargs):
    if instance.id is not None:  # new object will be created
        previous = Article.objects.get(id=instance.id)
        if previous.moderated != instance.moderated:  # field will be updated
            Notification.objects.get_or_create(notification_type=5, to_user=instance.user, object_id=instance.id,
                                               user_has_seen=False)

