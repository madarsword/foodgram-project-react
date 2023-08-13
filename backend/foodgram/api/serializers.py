from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from .fields import Base64ImageField
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Favorite,
    ShoppingCart,
)


class UserCreateSerializer(UserCreateSerializer):
    pass


class UserSerializer(UserSerializer):
    pass


class TagSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'pk',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        required=False,
        allow_null=True
    )
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = (
            'pk',
            'name',
            'image',
            'cooking_time',
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        required=False,
        allow_null=True
    )
    author = UserSerializer(read_only=True)
    tags = TagSerialiser(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, read_only=True, source='recipes')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    

    class Meta:
        model = Recipe
        fields = (
            'pk', 'tags', 'author',
            'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image',
            'text', 'cooking_time',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (
            request and request.user.is_authenticated
            and Favorite.objects.filter(
            user=request.user, recipe=obj
            ).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            request and request.user.is_authenticated
            and ShoppingCart.objects.filter(
            user=request.user, recipe=obj
            ).exists())
       

class RecipeCreateSerializer():
    pass