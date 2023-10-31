from django.contrib import admin
from django.contrib.admin import register

from .models import Subscribe


@register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
