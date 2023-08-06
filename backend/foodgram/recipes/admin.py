from django.contrib import admin

from recipes.models import (Tag, Ingredient, Recipe,
                            RecipeIngredient, Favorite, ShoppingCart)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    ordering = ('color',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('measurement_unit',)
    empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'text',
                    'cooking_time', 'pub_date',)
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'
    inlines = [
        RecipeIngredientInline,
    ]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'