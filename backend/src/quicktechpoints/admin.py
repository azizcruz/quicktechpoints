from django.contrib import admin
from .models import Article, Tag
from django.db import models


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'is_published_to_twitter', 'is_published_to_facebook')
    list_filter = ('title', 'is_published', 'is_published_to_twitter', 'is_published_to_facebook')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)