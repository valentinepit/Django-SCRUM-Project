from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from mainapp.forms import CommentForm
from mainapp.models import Article, Category, Tag, Comment
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
        'popular_tags': tags[:5],
        'best_of_week': best_of_week
    }
    return render(request, 'mainapp/index.html', context)


def category(request, pk, page=1):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if pk == 0:
        category_articles = Article.objects.all()
        current_category = {
            'title': 'Все потоки',
            'pk': 0
        }
    else:
        current_category = get_object_or_404(Category, pk=pk)
        category_articles = Article.objects.filter(category__pk=current_category.pk)

    newest_article = Article.objects.all().last()
    articles = Article.objects.all().order_by('-id')

    items_on_page = 10
    paginator = Paginator(category_articles, items_on_page)
    try:
        articles_paginator = paginator.page(page)
    except PageNotAnInteger:
        articles_paginator = paginator.page(1)
    except EmptyPage:
        articles_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'category_name',
        'categories': categories,
        'tags': tags[:10],
        'current_category': current_category,
        # 'category_articles': category_articles,
        'category_articles': articles_paginator,
        'newest_article': newest_article,
        'last_3_articles': articles[:3],
        'range': range(1, paginator.num_pages + 1)
    }

    return render(request, 'mainapp/category.html', context)


def article(request, pk):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    article = get_object_or_404(Article, pk=pk)
    similar_articles = Article.objects.filter(category__pk=article.category.pk).exclude(pk=article.pk)
    newest_article = Article.objects.all().last()
    articles = Article.objects.all().order_by('-id')
    tags = Tag.objects.all()
    total_likes = article.total_likes()

    comments = Comment.objects.filter(article__pk=article.pk)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'title': 'article_name',
        'article': article,
        'categories': categories,
        'popular_tags': tags[:5],
        'similar_articles': similar_articles[:2],
        'newest_article': newest_article,
        'last_3_articles': articles[:3],
        'tags': tags[:10],
        'commnets': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'total_likes': total_likes,
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


@login_required
def like(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return redirect('mainapp:article', pk=pk)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        article = get_object_or_404(Article, id=pk)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)

        context = {
            'article': article,
            'total_likes': article.total_likes
        }

        result = render_to_string('mainapp/includes/inc_likes.html',context)
        return JsonResponse({'result': result})
