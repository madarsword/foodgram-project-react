from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        null=False,
        blank=False,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=(validate_username,),
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        null=False,
        blank=False,
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        null=False,
        blank=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} {self.email}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_subscription',
            )
        ]
    
    def __str__(self):
        return f'{self.user} подписан на {self.author}'
