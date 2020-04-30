from django.contrib import admin
from .models import Profile, CustomUser, Contact


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('username', 'email')
    ordering = ('created',)
    list_per_page = 20


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo')
    list_filter = ('created', 'updated')
    search_fields = ('user',)
    ordering = ('created',)
    list_per_page = 20


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to')
    list_filter = ('created',)
    search_fields = ('user_from', 'user_to')
    ordering = ('created',)
    list_per_page = 20
