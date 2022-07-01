from django.contrib import admin
from personal_account.models import User, Notification
from mainapp.models import Category, Like, Comment, Article, Tag

admin.site.register(User)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(Notification)
