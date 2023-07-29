from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
        null=False,
        blank=False
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(validate_username,),
        verbose_name='Имя пользователя',
        null=False,
        blank=False
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        null=False,
        blank=False
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        null=False,
        blank=False
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        null=False,
        blank=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk',)

    def __str__(self):
        return f'{self.username} {self.email}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_follow',
            )
        ]
    
    def __str__(self):
        return f'{self.user} подписан на {self.author}'
