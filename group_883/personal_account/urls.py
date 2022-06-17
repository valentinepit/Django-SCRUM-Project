from django.urls import path
from personal_account.views import register, edit, login, logout, user, CreateArticle, EditArticle, ListArticle, \
    DeleteArticle

app_name = 'personal_account'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('user/', user, name='user'),
    path('list_article/', ListArticle.as_view(), name='list_article'),
    path('list_article/edit_article/<int:pk>/', EditArticle.as_view(), name='edit_article'),
    path('list_article/delete_article/<int:pk>/', DeleteArticle.as_view(), name='delete_article'),
    path('list_article/create_article/', CreateArticle.as_view(), name='create_article'),
]
