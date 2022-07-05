from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView
from mainapp.forms import CommentForm
from mainapp.models import Article, Category, Tag, Comment
from personal_account.models import User


def index(request):
    categories = Category.objects.all()
    articles = Article.objects.filter(is_active=True)
    read_now = articles
    news = Article.objects.filter(is_active=True).order_by('-created_at')[:5]
    tags = Tag.objects.all()
    best_of_week = articles
    best_authors = User.objects.order_by('-total_likes', '-id')[:5]
    context = {
        'title': 'Home',
        'categories': categories,
        'articles': articles,
        'read_now': read_now,
        'news': news,
        'tags': tags[:10],
        'best_of_week': best_of_week,
        'best_authors': best_authors,
        'popular_tags': get_popular_tags(),
    }
    return render(request, 'mainapp/index.html', context)


def get_popular_tags():
    _articles = Article.objects.filter(is_active=True)
    popular_articles = _articles.annotate(count=Count('likes')).order_by('-count', '-id').values('tag', 'tag__title')
    popular_tags = popular_articles.order_by('tag__title').distinct()
    tags = {}
    for item in popular_tags:
        tags[item["tag"]] = item["tag__title"]
    return tags


def category(request, pk, page=1):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if pk == 0:
        category_articles = Article.objects.filter(is_active=True)
        current_category = {
            'title': 'Все потоки',
            'pk': 0
        }
    else:
        current_category = get_object_or_404(Category, pk=pk)
        category_articles = Article.objects.filter(category__pk=current_category.pk).filter(is_active=True)

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
        'range': range(1, paginator.num_pages + 1),
        'popular_tags': get_popular_tags(),
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

    comments = Comment.objects.filter(article__pk=article.pk, is_parent=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            if new_comment.body.startswith('@moderator'):
                print("Модератора сюда")  # Нужны уведомления
    else:
        comment_form = CommentForm()

    context = {
        'title': 'article_name',
        'article': article,
        'categories': categories,
        'similar_articles': similar_articles[:2],
        'newest_article': newest_article,
        'last_3_articles': articles[:3],
        'tags': tags[:10],
        'commnets': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'popular_tags': get_popular_tags(),
    }
    return render(request, 'mainapp/article.html', context)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    print(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'mainapp/comment_form.html'
    form_class = CommentForm

    def get_success_url(self):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return reverse('mainapp:article', args=[comment.article.pk])


@login_required
def comment_create(request, article_pk, pk):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        context = {
            'form': comment_form,
            'popular_tags': get_popular_tags(),
        }

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = Article.objects.get(pk=article_pk)
            new_comment.user = request.user
            new_comment.parent = Comment.objects.get(pk=pk)
            new_comment.is_parent = False
            new_comment.save()
            if new_comment.body.startswith('@moderator'):
                print("Модератора сюда")  # Нужны уведомления
            return HttpResponseRedirect(reverse('mainapp:article', args=[new_comment.article.pk]))
    else:
        comment_form = CommentForm()
        context = {
            'form': comment_form,
            'popular_tags': get_popular_tags(),
        }
    return render(request, 'mainapp/comment_form.html', context)


@login_required
def moderation_list(request):
    categories = Category.objects.all()
    articles_to_moderate = Article.objects.filter(moderated=0).filter(is_active=True)
    context = {
        'categories': categories,
        'articles_to_moderate': articles_to_moderate,
        'popular_tags': get_popular_tags(),
    }
    return render(request, 'mainapp/moderation_list.html', context)


@login_required
def article_to_moderate(request, pk):
    categories = Category.objects.all()
    article = get_object_or_404(Article, pk=pk)
    context = {
        'categories': categories,
        'article': article,
        'popular_tags': get_popular_tags(),
    }
    return render(request, 'mainapp/article_to_moderate.html', context)


@login_required
def accept_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.moderated = 1
    article.save()

    return HttpResponseRedirect(reverse('mainapp:moderation_list'))


@login_required
def reject_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.moderated = 2
    article.save()

    return HttpResponseRedirect(reverse('mainapp:moderation_list'))

def help(request):
    categories = Category.objects.all()
    newest_article = Article.objects.all().last()
    articles = Article.objects.all().order_by('-id')
    context = {
        'title': 'help',
        'categories': categories,
        'newest_article': newest_article,
        'last_3_articles': articles[:3],
        'popular_tags': get_popular_tags(),
    }
    return render(request, 'mainapp/help.html', context)
