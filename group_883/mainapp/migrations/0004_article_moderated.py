# Generated by Django 4.0.3 on 2022-07-01 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='moderated',
            field=models.SmallIntegerField(default=0, verbose_name='Статус модерации'),
        ),
    ]
