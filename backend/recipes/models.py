from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=100
    )
    measurement_unit = models.CharField(
        verbose_name='единица измерения',
        max_length=50
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

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


class IngredientRecipe(models.Model):
    # recipe = models.ForeignKey(
    #     'Recipe',
    #     verbose_name='рецепт',
    #     on_delete=models.CASCADE,
    # )
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='рецепт',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='ингредиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='количество',
    )

    class Meta:
        verbose_name = 'ингредиент рецепта'
        verbose_name_plural = 'ингредиенты рецепта'
        # unique_together = ('ingredient', 'recipe')

    def __str__(self):
        return (f'{self.ingredient.name}: {self.amount} '
                f'{self.ingredient.measurement_unit}')


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
    ingredients = models.ManyToManyField(
        # IngredientRecipe,
        Ingredient,
        verbose_name='ингредиенты рецепта',
        related_name='ingredients_recipe',
        through='IngredientRecipe',
        # through='IngredientRecipe',
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
        return (f'Название: {self.name} | автор: {self.author.username} '
                f'| дата публикации: {self.pub_date:%d.%m.%Y %H:%M}')


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
        return (f'Пользователь: {self.user.username} | '
                f'рецепт: {self.recipe.name}')


# class ShoppingList(models.Model):
#     recipes = models.ManyToManyField(
#         Recipe,
#         verbose_name='рецепты'
#     )
#     # recipe = models.ForeignKey(
#     #     Recipe,
#     #     on_delete=models.CASCADE,
#     #     verbose_name='рецепт',
#     #     related_name='shopping_list_recipe',
#     # )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name='пользователь',
#     )

#     class Meta:
#         verbose_name = 'список покупок'
#         verbose_name_plural = 'списки покупок'

#     def __str__(self):
#         return f'Список покупок {self.user}'
