from django.contrib.admin import ListFilter
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from mainapp.models import Article, Category, Tag, Comment
from mainapp.forms import CommentForm
from django.views.generic import ListView
from personal_account.models import User
from .filters import ArticleFilter


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

    if article.likes.filter(id=request.user.id).exists():
        liked = True
    else:
        liked = False

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
        # 'total_likes': total_likes,
        'liked': liked,
        'comment_form': comment_form,
    }
    return render(request, 'mainapp/article.html', context)


class AuthorArticle:

    def get_Article(self):
        return Article.objects.filter(is_active=True)


class SearchResultsView(AuthorArticle, ListView):
    model = Article
    template_name = 'article_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if not query:
            query = ""
        articles = Article.objects.filter(title__icontains=query)
        myFilter = ArticleFilter(self.request.GET, queryset=articles)
        articles = myFilter.qs
        context.update({
            'search_data': query,
            'categories': Category.objects.order_by('title'),
            'count': len(Article.objects.filter(title__icontains=query)),
            'time_filter': ['За последний день', 'За последнюю неделю', 'За последний месяц', 'За все время'],
            'myFilter': myFilter,
            'articles': articles,

        })
        return context


    # def get_queryset(self):
    #     query = None
    #     if self.request.method == "GET":
    #         query = self.request.GET.get('q')
    #     if not query:
    #         query = ""
    #
    #     result = Article.objects.filter(
    #                 Q(category__title__in=self.category_filter()),
    #                 Q(created_at__gte=self.date_filter()),
    #                 Q(title__icontains=query)
    #             )
    #     return result

    # def category_filter(self):
    #     if self.request.GET.get('category') == '' or not self.request.GET.get('category'):
    #         categories = [item.get('title') for item in Category.objects.values('title')]
    #     else:
    #         categories = self.request.GET.getlist('category')
    #     return categories
    #
    # def date_filter(self):
    #     _date_filter = self.request.GET.get('date')
    #     today = timezone.now()
    #     days_gap = 0
    #     if _date_filter == "За все время" or not _date_filter:
    #         date_range = Article.objects.all().order_by('created_at').reverse()[:1].values()[0]["created_at"]\
    #                      - timedelta(days=1)
    #         return date_range
    #     if _date_filter == 'За последний день':
    #         days_gap = 1
    #     elif _date_filter == 'За последнюю неделю':
    #         days_gap = 7
    #     elif _date_filter == 'За последний месяц':
    #         days_gap = 30
    #     date_range = today - timedelta(days=days_gap)
    #     return date_range


class JsonFilterMoviesView(SearchResultsView, ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        query = None
        if self.request.method == "GET":
            query = self.request.GET.get('q')
        if not query:
            query = ""
        result = Article.objects.filter(
                    Q(category__title__in=self.category_filter()),
                    Q(created_at__gte=self.date_filter()),
                    Q(title__icontains=query)
                ).distinct().values("title")
        return result

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"articles": queryset}, safe=False)

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
            liked = False
            article.likes.remove(request.user)
        else:
            liked = True
            article.likes.add(request.user)

        context = {
            'article': article,
            'total_likes': article.total_likes,
            'liked': liked,
        }

        result = render_to_string('mainapp/includes/inc_likes.html', context)
        return JsonResponse({'result': result})
