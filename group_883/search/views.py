from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Count

from mainapp.views import SearchResultsView
from mainapp.models import Article, Category


# Create your views here.


class PopularListView(SearchResultsView):
    model = Article

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        query = ''
        context.update({
            'search_data': query,
            'categories': Category.objects.order_by('title'),
            'count': len(Article.objects.filter(title__icontains=query)),
        })
        return context

    def get_queryset(self):
        return super().get_queryset().annotate(count=Count('likes')).order_by('-count', '-id')
