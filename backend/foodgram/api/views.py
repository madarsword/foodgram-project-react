from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, HttpResponse
from django.db.models import Sum
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .filters import IngredientFilter, RecipeFilter
from .functions import adding_recipe, deleting_recipe
from .permissions import IsAdminAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    TagSerialiser,
    UserSubscriptionGetSerializer,
    UserSubscriptionSerializer,
    RecipeGetSerializer,
    RecipeCreateSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
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


class UserSubscriptionGetViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSubscriptionGetSerializer

    def get_queryset(self):
        return User.objects.filter(subscription__user=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class UserSubscriptionView(APIView):
    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        serializer = UserSubscriptionSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if not Subscription.objects.filter(
            user=request.user,
            author=author
            ).exists():
            return Response(
                {'errors': 'Вы не подписаны на этого автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.get(
            user=request.user.id,
            author=user_id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=('post', 'delete',),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return adding_recipe(request, recipe, FavoriteSerializer)

        if request.method == 'DELETE':
            error_message = 'Нет такого рецепта в избранном'
            return deleting_recipe(
                request,
                Favorite,
                recipe,
                error_message,
            )

    @action(
        detail=True,
        methods=('post', 'delete',),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return adding_recipe(
                request,
                recipe,
                ShoppingCartSerializer,
            )
        if request.method == 'DELETE':
            error_message = 'Нет такого рецепта в списке покупок'
            return deleting_recipe(
                request,
                ShoppingCart,
                recipe,
                error_message
            )

    @action(
        detail=False,
        methods=('get'),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount'))
        shopping_list = ['Список покупок:\n']
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_amount']
            shopping_list.append(f'\n{name} - {amount}, {unit}')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_cart.txt"'
        return response
