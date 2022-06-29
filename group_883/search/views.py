from .filters import ArticleFilter

from django.views.generic import ListView
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

    def get_queryset(self):
        queryset = super().get_queryset()
        return ArticleFilter(self.request.GET, queryset=queryset).qs

# @api_view(['GET', ])
# def my_function_based_list_view(request):
#     paginator = PageNumberPagination()
#     filtered_set = filters.MyModelFilter(
#         request.GET,
#         queryset=MyModel.objects.all()
#     ).qs
#     context = paginator.paginate_queryset(filtered_set, request)
#     serializer = MyModelSerializer(context, many=True)
#     return paginator.get_paginated_response(serializer.data)


class PopularListView(SearchResultsView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = context['articles'].annotate(count=Count('likes')).order_by('-count', '-id')
        return context
