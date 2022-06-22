from django.urls import path
from . import views as search

app_name = 'search'

urlpatterns = [
    path('', search.SearchResultsView.as_view(), name='search_results'),
]
