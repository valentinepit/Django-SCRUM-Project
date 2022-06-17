from datetime import timedelta
from django.utils import timezone

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
        query = None
        if self.request.method == "GET":
            query = self.request.GET.get('q')
        if not query:
            query = ""
        category_filter = self.category_filter()
        date_filter = self.date_filter(category_filter)
        result = date_filter.filter(title__icontains=query)
        return result

    def category_filter(self):
        cat_filter = self.request.GET.getlist('category') if self.request.GET.getlist('category') else "on"
        if "on" not in cat_filter:
            return Article.objects.filter(category__title__in=cat_filter)
        return Article.objects.all()

    def date_filter(self, _query):
        date_filter = "Anytime" if not self.request.GET.get('date') else self.request.GET.get('date')
        today = timezone.now()
        days_gap = 0
        if "Anytime" == date_filter:
            return _query.all()
        if date_filter == 'Today':
            days_gap = 1
        elif date_filter == 'Last Week':
            days_gap = 7
        elif date_filter == 'Last Month':
            days_gap = 30
        date_range = today - timedelta(days=days_gap)
        return _query.filter(created_at__gte=date_range)


def help(request):
    categories = Category.objects.all()
    newest_article = Article.objects.all().last()
    articles = Article.objects.all().order_by('-id')
    context = {
        'title': 'help',
        'categories': categories,
        'newest_article': newest_article,
        'last_3_articles': articles[:3],
    }
    return render(request, 'mainapp/help.html', context)
