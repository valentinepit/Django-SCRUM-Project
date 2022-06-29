import django_filters
from django import forms

from mainapp.models import *


class ArticleFilter(django_filters.FilterSet):
    tag = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Article
        fields = {
            'category': ['exact'],
            'user': ['exact'],
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
