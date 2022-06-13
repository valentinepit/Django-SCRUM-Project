from django.shortcuts import render, get_object_or_404

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


def category(request, pk):
    context = {
        'title': 'category_name'
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
        'comment_form': comment_form
    }
    return render(request, 'mainapp/article.html', context)


class SearchResultsView(ListView):
    model = Article
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Article.objects.filter(title__icontains=query)

