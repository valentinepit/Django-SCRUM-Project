from django.urls import path
from . import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index')
]

