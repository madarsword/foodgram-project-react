from datetime import datetime as dt

from django.shortcuts import HttpResponse
from rest_framework import response, status
from rest_framework.generics import get_object_or_404

from recipes.models import Recipe


def add_remove(add_serializer, model, request, recipe_id):
    user = request.user
    data = {'user': user.id,
            'recipe': recipe_id}
    serializer = add_serializer(data=data, context={'request': request})
    if request.method == 'POST':
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data,
                                 status=status.HTTP_201_CREATED)
    get_object_or_404(
        model, user=user, recipe=get_object_or_404(Recipe, id=recipe_id)
    ).delete()
    return response.Response(status=status.HTTP_204_NO_CONTENT)

def shopping_list(self, request, ingredients):
    user = self.request.user
    filename = f'{user.username}_shopping_list.txt'
    today = dt.today()
    shopping_list = (
        f'Список покупок {user.username}\n\n'
        f'Дата: {today:%Y-%m-%d}\n\n'
    )
    shopping_list += '\n'.join([
        f'- {ingredient["ingredient__name"]} '
        f'({ingredient["ingredient__measurement_unit"]})'
        f' - {ingredient["amount"]}'
        for ingredient in ingredients
    ])
    shopping_list += f'\n\nFoodgram ({today:%Y})'
    response = HttpResponse(
        shopping_list, content_type='text.txt; charset=utf-8'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
