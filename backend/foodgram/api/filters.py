from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe, Tag, Ingredient
from users.models import User


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart_filter'
    )

    def get_is_favorite_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def get_is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(carts__user=user)
        return queryset
    
    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
