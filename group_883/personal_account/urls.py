from django.urls import path
from personal_account.views import register, edit, login, logout

app_name = 'personal_account'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
]
