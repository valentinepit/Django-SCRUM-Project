from . import views
from django.urls import path

app_name = 'rating'

urlpatterns = [
    path('<int:pk>/', views.like, name='like_article'),
    path('comment/<int:pk>/', views.like_comment, name='like_comment'),
]
