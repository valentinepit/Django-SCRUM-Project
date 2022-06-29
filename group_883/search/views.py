from .filters import ArticleFilter

from django.views.generic import ListView
from django.db.models import Count

from mainapp.models import Article, Tag
from mainapp.views import get_popular_tags


class SearchResultsView(ListView):
    model = Article
    template_name = 'search.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if not query:
            query = ""
        articles = Article.objects.filter(title__icontains=query).filter(is_active=True)
        my_filter = ArticleFilter(self.request.GET, queryset=articles)
        filter_data = my_filter.qs
        context.update({
            'search_data': query,
            'count': len(Article.objects.filter(title__icontains=query)),
            'myFilter': my_filter,
            'articles': filter_data,
            'popular_tags': get_popular_tags(Article.objects.filter(is_active=True)),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return ArticleFilter(self.request.GET, queryset=queryset).qs


class PopularListView(SearchResultsView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = context['articles'].annotate(count=Count('likes')).order_by('-count', '-id')
        return context
