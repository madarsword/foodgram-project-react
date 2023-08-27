import json

from foodgram.settings import BASE_DIR

from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Выгрузка ингредиентов из ingredients.json"

    def handle(self, *args, **kwargs):
        file = f"{BASE_DIR}/data/ingredients.json"
        with open(file, "r",
                  encoding="utf-8") as file:
            reader = json.load(file)
        for ingredient in reader:
            Ingredient.objects.get_or_create(**ingredient)
        self.stdout.write(self.style.SUCCESS("Ингредиенты выгружены!"))
