from django.urls import include, path
from rest_framework import routers

from .views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
    UserSubscriptionGetViewSet,
    UserSubscriptionView,
)


router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('users/subscriptions/',
         UserSubscriptionGetViewSet.as_view({'get': 'list'})),
    path('users/<int:user_id>/subscribe/',
         UserSubscriptionView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
