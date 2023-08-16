from django.contrib import admin

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Favorite,
    ShoppingCart,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    list_filter = ('name', 'color', 'slug',)
    search_fields = ('name', 'color', 'slug',)
    ordering = ('name',)
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
    list_display = (
        'name',
        'author',
        'text',
        'cooking_time',
        'favorites_count',
        'get_tags',
        'pub_date',
    )
    readonly_fields = ('favorites_count',)
    search_fields = ('name', 'author',)
    list_filter = ('name', 'author', 'tags',)
    empty_value_display = '-пусто-'
    inlines = (RecipeIngredientInline,)

    @admin.display(description='Количество в избранном')
    def favorites_count(self, obj):
        return obj.favorites.count()
    
    @admin.display(description='Теги')
    def get_tags(self, obj):
        return ', '.join(_.name for _ in obj.tags.all())


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = ('recipe', 'ingredient')
    search_fields = ('recipe', 'ingredient')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe',)
    empty_value_display = '-пусто-'
