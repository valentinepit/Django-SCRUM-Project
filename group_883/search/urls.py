from django.urls import path
from . import views as search

app_name = 'search'

urlpatterns = [
    path('popular/', search.PopularListView.as_view(), name='popular'),

    path('', search.SearchResultsView.as_view(), name='search_results'),
    path('<int:pk>', search.SearchResultsView.as_view(), name='search_results_with_pk'),
    # path('tags/(?P<pk>[0-9]+)\\', search.SearchByTagView.as_view(), name='search_by_tag'),
    # path('tags/<int:pk>', search.SearchByTagView.as_view(), name='search_by_tag'),

]
