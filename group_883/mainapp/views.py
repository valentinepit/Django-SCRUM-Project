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
    read_now = Article.objects.all()
    news = Article.objects.all()
    tags = Tag.objects.all()
    best_of_week = Article.objects.all()
    best_authors = User.objects.order_by('-total_likes', '-id')[:5]
    popular_tags = get_popular_tags(articles)
    context = {
        'title': 'Home',
        'categories': categories,
        'articles': articles,
        'read_now': read_now,
        'news': news,
        'tags': tags[:10],
        'best_of_week': best_of_week,
        'best_authors': best_authors,
        'popular_tags': popular_tags,
    }
    return render(request, 'mainapp/index.html', context)


def get_popular_tags(_articles):
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
        category_articles = Article.objects.all()
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
        'popular_tags': tags[:5],
        'similar_articles': similar_articles[:2],
        'newest_article': newest_article,
        'last_3_articles': articles[:3],
        'tags': tags[:10],
        'commnets': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'mainapp/article.html', context)


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


def comment_create(request, article_pk, pk):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        context = {
            'form': comment_form
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
            'form': comment_form
        }
    return render(request, 'mainapp/comment_form.html', context)


# class SearchResultsView(ListView):
#     model = Article
#     template_name = 'search.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(SearchResultsView, self).get_context_data(**kwargs)
#         query = self.request.GET.get('q')
#         context.update({
#             'search_data': query,
#             'categories': Category.objects.order_by('title'),
#             'count': len(Article.objects.filter(title__icontains=query)),
#         })
#         return context
#
#     def get_queryset(self):
#         query = None
#         if self.request.method == "GET":
#             query = self.request.GET.get('q')
#         if not query:
#             query = ""
#         category_filter = self.category_filter()
#         date_filter = self.date_filter(category_filter)
#         result = date_filter.filter(title__icontains=query)
#         return result
#
#     def category_filter(self):
#         cat_filter = self.request.GET.getlist('category') if self.request.GET.getlist('category') else "on"
#         if "on" not in cat_filter:
#             return Article.objects.filter(category__title__in=cat_filter)
#         return Article.objects.all()
#
#     def date_filter(self, _query):
#         date_filter = "Anytime" if not self.request.GET.get('date') else self.request.GET.get('date')
#         today = timezone.now()
#         days_gap = 0
#         if "Anytime" == date_filter:
#             return _query.all()
#         if date_filter == 'Today':
#             days_gap = 1
#         elif date_filter == 'Last Week':
#             days_gap = 7
#         elif date_filter == 'Last Month':
#             days_gap = 30
#         date_range = today - timedelta(days=days_gap)
#         return _query.filter(created_at__gte=date_range)


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
