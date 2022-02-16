from django.contrib.auth import get_user_model
# from django.db.models import F
# from rest_framework.generics import get_object_or_404
# from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer)

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
# from users.serializers import UserSerializer

User = get_user_model()


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeSerializer(ModelSerializer):
    id = IntegerField(source='ingredient.id')
    name = CharField(source='ingredient.name')
    measurement_unit = CharField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ShortRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AddIngredientToRecipeSerializer(ModelSerializer):
    id = IntegerField()
    # amount = IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


# class CreateRecipeSerializer(ModelSerializer):
#     tags = PrimaryKeyRelatedField(
#         many=True,
#         queryset=Tag.objects.all()
#     )
#     ingredients = AddIngredientToRecipeSerializer(many=True)

#     class Meta:
#         model = Recipe
#         fields = ('recipe', 'user')

#     def create(self, validated_data):
#         ingredients = validated_data.pop('ingredients')
#         tags = validated_data.pop('tags')
#         for ingredient in ingredients:
#             if Ingredient['amount'] <= 0:
#                 raise ValidationError(
#                     'Количество ингредиента не может быть '
#                     'отрицательным числом или нулём'
#                 )
#         recipe = Recipe.objects.create(**validated_data)
#         recipe.tags.set(tags)
#         for ingredient in ingredients:
#             object = get_object_or_404(Ingredient, id=ingredient['id'])
#             amount = ingredient['amount']
#             if IngredientRecipe.objects.filter(
#                 recipe=recipe,
#                 ingredient=object
#             ).exists():
#                 amount += F('amount')
#             IngredientRecipe.objects.update_or_create(
#                 recipe=recipe,
#                 ingredient=object,
#                 defaults={'amount': amount}
#             )
#         return recipe


# class FavoriteRecipeSerializer(ModelSerializer):
#     class Meta:
#         model = Favorite
#         fields = ('recipe', 'user')
