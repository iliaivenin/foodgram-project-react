from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingridient(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=100
    )
    measurement_unit = models.CharField(
        verbose_name='единица измерения',
        max_length=50
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=50
    )
    color = models.CharField(
        verbose_name='цвет',
        max_length=7
    )
    slug = models.SlugField(
        verbose_name='слаг',
        unique=True
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name='название',
        max_length=200,
    )
    image = models.ImageField(
        upload_to=settings.UPLOAD_FOLDER,
        verbose_name='изображение',
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name='описание рецепта',
    )
    ingridients = models.ManyToManyField(
        Ingridient,
        verbose_name='ингридиент',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='тег',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        OUTPUT = ('Название: {name} | автор: {author} '
                  'дата публикации: {pub_date:%d.%m.%Y %H:%M}')
        return OUTPUT.format(name=self.name, author=self.author.username,
                             pub_date=self.pub_date)


class IngridientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        on_delete=models.CASCADE,
    )
    ingridient = models.ForeignKey(
        Ingridient,
        verbose_name='ингридиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='количество',
    )

    class Meta:
        verbose_name = 'ингридиент рецепта'
        verbose_name_plural = 'ингридиенты рецепта'

    def __str__(self):
        pass


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        related_name='following',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follower'
            )
        ]

    def __str__(self):
        OUTPUT = 'Пользователь: {user} | автор: {author}'
        return OUTPUT.format(user=self.user.username,
                             author=self.author.username)


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        related_name='favorited_recipe',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        related_name='favorited_by_user',
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe'
            )
        ]

    def __str__(self):
        OUTPUT = 'Пользователь: {user} | рецепт: {recipe}'
        return OUTPUT.format(user=self.user.username,
                             recipe=self.recipe.name)


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'список покупок'

    def __str__(self):
        return f'Список покупок {self.recipe.name}'
