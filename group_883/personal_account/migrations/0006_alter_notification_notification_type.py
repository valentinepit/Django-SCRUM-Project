# Generated by Django 4.0.3 on 2022-07-01 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_account', '0005_remove_notification_article_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(0, '@moderator'), (1, 'Like_Article'), (2, 'Comment'), (3, 'Like_Comment'), (4, 'Reply')], verbose_name='Тип'),
        ),
    ]
