from django.contrib import admin
from tags.models import Tag

from .models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                     ShoppingCart)


class BaseAdminSettings(admin.ModelAdmin):
    """Админ панель."""
    empty_value_display = 'empty'
    list_filter = ('author', 'name', 'tags')


class IngredientAdmin(BaseAdminSettings):
    """
    Админ панель ингредиентов.
    """
    list_display = (
        'name',
        'measurement_unit'
    )

    list_filter = ('name',)


class RecipeAdmin(BaseAdminSettings):
    """
    Админ панель рецептов.
    """
    list_display = (
        'name',
        'author',
        'added_in_favorites'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    filter_horizontal = ('tags',)
    readonly_fields = ('added_in_favorites',)

    def added_in_favorites(self, obj):
        return obj.favorited_by.count()
    added_in_favorites.short_description = 'Количество добавлений в избранное'


class RecipeIngredientsAdmin(admin.ModelAdmin):
    """
    Админ панель управления.
    """
    list_display = (
        'ingredient',
        'amount',
    )
    list_filter = ('ingredient',)


class ShoppingCartAdmin(admin.ModelAdmin):
    """
    Админ панель списка покупок.
    """
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('user',)


class TagAdmin(BaseAdminSettings):
    """
    Админ панель тегов.
    """
    list_display = (
        'name',
        'color',
        'slug'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    """
    Админ панель избранных рецептов.
    """
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('recipe', 'user')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
