# # from djoser.serializers import UserSerializer
# from rest_framework import serializers
# from rest_framework.generics import get_object_or_404
# from rest_framework.serializers import ModelSerializer

# from recipes.models import (Favorite, Subscription, IngredientRecipe, Ingredient,
#                             Recipe, ShoppingCart, Tag, User)


# class IngredientSerializer(ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurment_unit')


# class TagSerializer():
#     class Meta:
#         model = Tag
#         fields = '__all__'


# class AddIngredientToRecipeSerializer():
#     pass


# class RecipeSerializer(ModelSerializer):
#     tags = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Tag.objects.all()
#     )
#     ingredients = AddIngredientToRecipeSerializer(many=True)

#     class Meta:
#         model = Recipe
#         fields = '__all__'
#         read_only_fields = ('author', )

#     def create(self, validated_data):
#         ingredients = validated_data.pop('ingredients')
#         tags = validated_data.pop('tags')
#         for ingredient in ingredients:
#             if ingredient['amount'] <= 0:
#                 raise serializers.ValidationError(
#                     'Количество ингредиента не может быть '
#                     'отрицательным числом или нулём'
#                 )
#         recipe = Recipe.objects.create(validated_data)
#         recipe.tags.set(tags)
#         for ingredient in ingredients:
#             obj get_object_or_404(Ingredient, id=ingredient['id'])