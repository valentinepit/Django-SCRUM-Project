import django_filters
from sqlalchemy.testing import exclude

from .models import *


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ['category', 'user', 'tag']
