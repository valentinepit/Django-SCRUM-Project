from django.shortcuts import render
from django.views.generic import ListView
from .models import Article


def index(request):
    context = {
        'title': 'Home'
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

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            query = ""
        return Article.objects.filter(title__icontains=query)

