from django.urls import path
from . import views as search

app_name = 'search'

urlpatterns = [
    path('popular/', search.PopularListView.as_view(), name='popular'),

    path('', search.SearchResultsView.as_view(), name='search_results'),
]
