from django.shortcuts import render
from mainapp.models import Article, Category, Tag


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

