from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo')
    #list_filter = ('created', 'updated')
    search_fields = ('user',)
    #ordering = ('created',)
    list_per_page = 20
