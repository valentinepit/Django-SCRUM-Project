import json

from django.core.management.base import BaseCommand
from django.conf import settings

from mainapp.models import Category, Article, Tag
from personal_account.models import User


def load_from_json(file_name):
    with open(f'{settings.BASE_DIR}/json/{file_name}.json', 'r', encoding='UTF-8') as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):

        Category.objects.all().delete()
        Article.objects.all().delete()
        Tag.objects.all().delete()
        User.objects.all().delete()

        tags = load_from_json('tags')
        for tag in tags:
            Tag.objects.create(**tag)

        users = load_from_json('users')
        for user in users:
            User.objects.create(**user)
        categories = load_from_json('categories')
        for category in categories:
            Category.objects.create(**category)

        articles = load_from_json('articles')

        for article in articles:
            category_name = article['category']
            category_item = Category.objects.get(title=category_name)
            article['category'] = category_item
            user_name = article['user']
            user_item = User.objects.get(username=user_name)
            article['user'] = user_item
            tag_name = article['tag']
            tag_item = Tag.objects.get(title=tag_name)
            article['tag'] = tag_item
            Article.objects.create(**article)
