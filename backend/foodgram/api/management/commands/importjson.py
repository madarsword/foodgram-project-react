import json
import os

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.db.utils import IntegrityError

from recipes.models import Ingredient


FILE_DIR = os.path.join(os.path.dirname(os.path.dirname(settings.BASE_DIR)), 'data')


def import_json():
    with open(
        os.path.join(FILE_DIR, 'ingredients.json'), encoding='utf-8'
    ) as data_file_ingredients:
        ingredient_data = json.loads(data_file_ingredients.read())
        for ingredients in ingredient_data:
            Ingredient.objects.get_or_create(**ingredients)
        print(f'Файл {data_file_ingredients.name} загружен')


class Command(BaseCommand):
    help = 'Импорт данных из json в базу данных'
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Начало выгрузки'))
        try:
            import_json()
        except IntegrityError:
            raise CommandError(
                'Очистите базу данных перед загрузкой файлов'
            )
        except FileNotFoundError:
            raise CommandError(
                'Файлы json не найдены'
            )
        except Exception:
            raise CommandError(
                'Неизвестная ошибка'
            )
        self.stdout.write(self.style.SUCCESS(
            'Все данные загружены в базу данных'
        ))
