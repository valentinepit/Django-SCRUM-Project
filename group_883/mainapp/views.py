from django.shortcuts import render
from mainapp.models import Article, Category, Tag
from django.views.generic import ListView

def index(request):
    categories = Category.objects.all()
    articles = Article.objects.all()
    read_now = Article.objects.all()
    news = Article.objects.all()
    tags = Tag.objects.all()
    best_of_week = Article.objects.all()

    context = {
        'title': 'Home',
        'categories': categories,
        'articles': articles,
        'read_now': read_now,
        'news': news,
        'tags': tags[:10],
        'best_of_week': best_of_week
    }
    return render(request, 'mainapp/index.html', context)


def category(request, pk):
    context = {
        'title': 'category_name'
    }
    return render(request, 'mainapp/category.html', context)


def article(request, pk):
    context = {
        'title': 'article_name'
    }
    return render(request, 'mainapp/article.html', context)


class SearchResultsView(ListView):
    model = Article
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context.update({
            'search_data': query,
            'categories': Category.objects.order_by('title'),
            'count': len(Article.objects.filter(title__icontains=query)),
        })
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            query = ""
        result = Article.objects.filter(title__icontains=query)
        return result

    def url_name(self, request):
        url_name = False
        if request.resolver_match:
            url_name = request.resolver_match.url_name
        return {"url_name": url_name}


