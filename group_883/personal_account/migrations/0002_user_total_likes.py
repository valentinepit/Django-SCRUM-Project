# Generated by Django 4.0.3 on 2022-06-23 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='total_likes',
            field=models.IntegerField(default=0, verbose_name='Кол-во лайков автора'),
        ),
    ]
