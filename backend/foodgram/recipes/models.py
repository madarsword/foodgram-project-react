from django.db import models


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=7,
        unique=True,
        null=False,
        blank=False
    )
    color = models.CharField(
        verbose_name='Цвет тега в HEX',
        max_length=7,
        unique=True,
        null=False,
        blank=False
    )
    slug = models.SlugField(
        verbose_name='Слаг тега',
        max_length=10,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, цвет: {self.color}'


class Recipe(models.Model):
    author =
    ingredients =
    tags =
    image = models.ImageField(
        upload_to='/',
        null=False,
        blank=False
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        null=False,
        blank=False
    )
    text = models.CharField(
        verbose_name='Текстовое описание рецепта',
        null=False,
        blank=False
    )
    cooking_time =


class Ingredient(models.Model):
    name =
    amount = 
    measurement_unit =


class Favorite(models.Model):
    name =
    image =
    cooking_time =


class Shopping_cart(models.Model):
