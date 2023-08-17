from django.shortcuts import get_object_or_404
from django.db.models import Sum
from djoser.views import UserViewSet
from rest_framework import (
    decorators,
    permissions,
    response,
    status,
    viewsets,
)
from urllib.parse import unquote

from .filters import RecipeFilter
from .functions import add_remove, shopping_list
from .pagination import PageLimitPagination
from .permissions import IsAdminAuthorOrReadOnly
from .serializers import (
    UserSerializer,
    SubscriptionSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeCreateSerializer,
    FavoriteAddSerializer,
    ShoppingCartAddSerializer,
)
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite,
    ShoppingCart,
    RecipeIngredient,
)
from users.models import User, Subscription


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageLimitPagination

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscription.objects.create(user=user, author=author)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        get_object_or_404(Subscription, user=user, author=author).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @decorators.action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        return self.get_paginated_response(
            SubscriptionSerializer(
                self.paginate_queryset(
                    User.objects.filter(following__user=request.user)
                ),
                many=True,
                context={'request': request},
            ).data
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None

    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = self.queryset
        if name:
            if name[0] == '%':
                name = unquote(name)
            else:
                name = name.translate(str.maketrans(
                    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
                    'йцукенгшщзхъфывапролджэячсмитьбю.'
                    )
                )
            name = name.lower()
            start_queryset = list(queryset.filter(name__istartswith=name))
            ingridients_set = set(start_queryset)
            cont_queryset = queryset.filter(name__icontains=name)
            start_queryset.extend(
                [ing for ing in cont_queryset if ing not in ingridients_set]
            )
            queryset = start_queryset
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly,)
    serializer_class = RecipeGetSerializer
    filterset_class = RecipeFilter
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeCreateSerializer
        return RecipeGetSerializer

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        return add_remove(
            FavoriteAddSerializer, Favorite, request, pk
        )

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        return add_remove(
            ShoppingCartAddSerializer, ShoppingCart, request, pk
        )

    @decorators.action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_list__user=self.request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).order_by('ingredient__name').annotate(amount=Sum('amount'))
        return shopping_list(self, request, ingredients)
