from .filters import ArticleFilter

from django.views.generic import ListView
from django.db.models import Count

from mainapp.models import Article


class SearchResultsView(ListView):
    model = Article
    template_name = 'search.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if not query:
            query = ""
        articles = Article.objects.filter(title__icontains=query)
        my_filter = ArticleFilter(self.request.GET, queryset=articles)
        context.update({
            'search_data': query,
            'count': len(Article.objects.filter(title__icontains=query)),
            'myFilter': my_filter,
            'articles': my_filter.qs,
        })
        return context


class PopularListView(SearchResultsView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = context['articles'].annotate(count=Count('likes')).order_by('-count', '-id')
        return context
