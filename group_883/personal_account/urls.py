from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required
from personal_account.views import register, edit, login, logout, CreateArticle, EditArticle, ListArticle, \
    DeleteArticle, password_change_done, UserDetail, user, verify, create_permissions, delete_permissions, delete_user, \
    PostNotification, FollowNotification, RemoveNotification, blocked, block_render

app_name = 'personal_account'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('our_user/<int:pk>/', UserDetail.as_view(), name='our_user'),
    path('user/', user, name='user'),
    path('list_article/', ListArticle.as_view(), name='list_article'),
    path('list_article/edit_article/<int:pk>/', login_required(EditArticle.as_view()), name='edit_article'),
    path('list_article/delete_article/<int:pk>/', login_required(DeleteArticle.as_view()), name='delete_article'),
    path('list_article/create_article/', login_required(CreateArticle.as_view()), name='create_article'),
    path('pasword_change/',
         PasswordChangeView.as_view(template_name='personal_account/password_change.html',
                                    success_url=reverse_lazy('personal_account:password_change_done')),
         name='password_change'),
    path('password_change/done/', password_change_done, name='password_change_done'),
    path('verify/<email>/<key>/', verify, name='verify'),
    path('moder_perm/<int:pk>/', create_permissions, name='create_permissions'),
    path('del_perm/<int:pk>/', delete_permissions, name='delete_permissions'),
    path('del_user/<int:pk>/', delete_user, name='delete_user'),
    path('block_user/<int:pk>/', blocked, name='blocked'),
    path('block/<int:pk>/', block_render, name='block_render'),

    path('notification/<int:notification_pk>/article/<int:article_pk>', PostNotification.as_view(),
         name='article-notification'),
    path('notification/<int:notification_pk>/profile/<int:profile_pk>', FollowNotification.as_view(),
         name='follow-notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),
]
