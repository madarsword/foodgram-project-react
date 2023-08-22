import csv
import os

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.db.utils import IntegrityError
from recipes.models import Ingredient

FILE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(settings.BASE_DIR)), 'data'
)


def import_csv():
    with open(
        os.path.join(FILE_DIR, 'ingredients.csv'), 'r', encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name, measurement_unit = row
            Ingredient.objects.get_or_create(
                name=name, measurement_unit=measurement_unit
            )
        print(f'Файл {csvfile.name} загружен')


class Command(BaseCommand):
    help = 'Импорт данных из csv в базу данных'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Начало выгрузки'))
        try:
            import_csv()
        except IntegrityError:
            raise CommandError(
                'Очистите базу данных перед загрузкой'
            )
        except FileNotFoundError:
            raise CommandError(
                'Файлы csv не найдены'
            )
        except Exception:
            raise CommandError(
                'Неизвестная ошибка'
            )

        self.stdout.write(self.style.SUCCESS(
            'Все данные загружены в базу данных'
        ))
