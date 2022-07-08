from .filters import ArticleFilter
from django.template.defaulttags import register

from django.views.generic import ListView
from django.db.models import Count

from mainapp.models import Article, Tag
from mainapp.views import get_popular_tags


class SearchResultsView(ListView):
    model = Article
    template_name = 'search.html'
    paginate_by = 3
    filter_set_class = ArticleFilter

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if not query:
            query = ""
        active_articles = Article.objects.filter(is_active=True).select_related()
        articles = active_articles.filter(title__icontains=query).filter(is_active=True)
        my_filter = self.filter_set_class(self.request.GET, queryset=articles)
        filter_data = my_filter.qs
        context.update({
            'count': len(filter_data),
            'search_data': query,
            'myFilter': my_filter,
            'articles': filter_data,
            'popular_tags': get_popular_tags(),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return ArticleFilter(self.request.GET, queryset=queryset).qs.filter(is_active=True)

    def get_filterset_kwargs(self, filter_set_class):
        kwargs = super(SearchResultsView, self).get_filterset_kwargs(filter_set_class)
        kwargs['attribute'] = 'width'
        return kwargs

    @register.filter
    def get_item(self, dictionary, key):
        return dictionary.get(key)


class SearchByTagView(SearchResultsView):

    def get_queryset(self):
        queryset = super().get_queryset().select_related()
        return ArticleFilter(self.request.GET, queryset=queryset).qs.filter(tag=self.kwargs['pk'])


class PopularListView(SearchResultsView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = context['articles'].annotate(count=Count('likes')).order_by('-count', '-id')
        return context
