from django.urls import path
from . import views as mainapp

from .views import SearchResultsView

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('category/<int:pk>/', mainapp.category, name='category'),
    path('article/<int:pk>/', mainapp.article, name='article'),
]

