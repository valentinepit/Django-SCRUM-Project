from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('category/<int:pk>/', mainapp.category, name='category'),
    path('category/<int:pk>/<int:page>/', mainapp.category, name='category_page'),
    path('article/<int:pk>/', mainapp.article, name='article'),
    path('help/', mainapp.help, name='help'),
    path('comment/remove/<int:pk>/', mainapp.comment_remove, name='comment_remove'),
    path('comment/update/<int:pk>/', login_required(mainapp.CommentUpdateView.as_view()), name='comment_update'),
    # path('comment/create/<int:article_pk>/<int:pk>/', mainapp.CommentCreateView.as_view(), name='comment_create')
    path('comment/create/<int:article_pk>/<int:pk>/', mainapp.comment_create, name='comment_create')
]
