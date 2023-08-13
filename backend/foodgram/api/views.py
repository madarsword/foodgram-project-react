from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django.db.models import Sum
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import HttpResponse, get_object_or_404

from .filters import RecipeFilter
from .pagination import PageLimitPagination
from .permissions import IsAdminAuthorOrReadOnly
from .serializers import (
    TagSerialiser,
    IngredientSerializer,
    RecipeSerializer,
    RecipeReadSerializer,
    RecipeCreateSerializer,
    UserSerializer,
    UserCreateSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
)   
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Favorite,
    ShoppingCart,
)
from users.models import User, Subscription


class UserViewSet():
    queryset = User.objects.all()
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        return UserCreateSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageLimitPagination
    permission_classes = (IsAdminAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateSerializer
    
    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])
        return self.toggle_favorite_or_cart(
            request, recipe, RecipeSerializer, Favorite.objects)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        return self.toggle_favorite_or_cart(
            request, recipe, RecipeSerializer, ShoppingCart.objects)

    @action(
        detail=False, methods=['get'],
        permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__shopping_recipe__user=request.user)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list(
                'ingredient__name', 'total_amount',
                'ingredient__measurement_unit')
        )
        wishlist = []
        for item in ingredients:
            wishlist.append(
                f'{item[0]} - {item[2]} {item[1]}'
            )
        wishlist = '\n'.join(wishlist)
        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response
