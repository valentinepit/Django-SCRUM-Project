from mainapp.models import Article
from django.views.generic import ListView
from .filters import ArticleFilter


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
        })
        print('new')
        return context

