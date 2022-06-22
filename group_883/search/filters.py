import django_filters

from mainapp.models import *


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            'category': ['exact'],
            'user': ['exact'],
            'tag': ['exact'],
            'created_at': ['lt', 'gt'],
        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }
