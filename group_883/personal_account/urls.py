from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required
from personal_account.views import register, edit, login, logout, user, CreateArticle, EditArticle, ListArticle, \
    DeleteArticle, password_change_done

app_name = 'personal_account'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('user/', user, name='user'),
    path('list_article/', ListArticle.as_view(), name='list_article'),
    path('list_article/edit_article/<int:pk>/', login_required(EditArticle.as_view()), name='edit_article'),
    path('list_article/delete_article/<int:pk>/', login_required(DeleteArticle.as_view()), name='delete_article'),
    path('list_article/create_article/', login_required(CreateArticle.as_view()), name='create_article'),
    path('pasword_change/',
         PasswordChangeView.as_view(template_name='personal_account/password_change.html',
                                    success_url=reverse_lazy('personal_account:password_change_done')),
         name='password_change'),
    path('password_change/done/', password_change_done, name='password_change_done')
]
