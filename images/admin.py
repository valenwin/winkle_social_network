from django.contrib import admin
from .models import Image, Comment


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image', 'created')
    list_filter = ('created',)
    search_fields = ('title', 'image')
    ordering = ('created',)
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'body')
    list_per_page = 20
