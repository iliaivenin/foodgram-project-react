from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import (CASCADE, BooleanField, CharField, DateTimeField,
                              EmailField, ForeignKey, ManyToManyField, Model,
                              UniqueConstraint)
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = EmailField(
        'адрес электропочты',
        max_length=254,
        unique=True
    )
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    is_active = BooleanField(default=True)
    date_joined = DateTimeField(default=timezone.now)
    username = CharField('юзернейм', max_length=150)
    first_name = CharField('имя', max_length=150)
    last_name = CharField('фамилия', max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


class Subscription(Model):
    user = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        verbose_name='пользователь',
        related_name='follower',
    )
    author = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        verbose_name='автор',
        related_name='following',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'], name='unique_follower'
            )
        ]

    def __str__(self):
        return (f'Пользователь: {self.user.username} | '
                f'автор: {self.author.username}')


class ShoppingCart(Model):
    recipes = ManyToManyField(
        'recipes.Recipe',
        verbose_name='рецепты',
    )
    user = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        verbose_name='пользователь',
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'

    def __str__(self):
        return f'Список покупок {self.user}'
