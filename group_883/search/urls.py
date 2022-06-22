from django.urls import path
from . import views


app_name = 'search'

urlpatterns = [
    path('popular/', views.PopularListView.as_view(), name='popular'),

]
