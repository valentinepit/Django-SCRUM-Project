from django.urls import path, include
from . import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('category/<int:pk>/', mainapp.category, name='category'),
    path('category/<int:pk>/<int:page>/', mainapp.category, name='category_page'),
    path('article/<int:pk>/', mainapp.article, name='article'),
    path('help/', mainapp.help, name='help'),
    path('like/<int:pk>/', mainapp.like, name='like_article')
]
