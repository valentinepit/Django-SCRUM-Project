from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string

from mainapp.models import Article


# Create your views here.
@login_required
def like(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return redirect('mainapp:article', pk=pk)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        article = get_object_or_404(Article, id=pk)
        if article.likes.filter(id=request.user.id).exists():
            with transaction.atomic():
                article.likes.remove(request.user)
                article.user.total_likes = F('total_likes') - 1
                article.user.save()
        else:
            with transaction.atomic():
                article.likes.add(request.user)
                article.user.total_likes = F('total_likes') + 1
                article.user.save()

        context = {
            'article': article,
        }
        result = render_to_string('rating/includes/inc_likes_js.html', context, request=request)
        return JsonResponse({'result': result})
