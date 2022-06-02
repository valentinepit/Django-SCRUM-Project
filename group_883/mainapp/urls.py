from django.urls import path
from . import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('category/<int:pk>/', mainapp.category, name='category'),
    path('article/<int:pk>/', mainapp.article, name='article'),
]

