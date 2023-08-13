from rest_framework import serializers

from recipes.models import (
    Tag, Ingredient,
)


class UserCreateSerializer():
    pass


class UserSerializer():
    pass


class TagSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
