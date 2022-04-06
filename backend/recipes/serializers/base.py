from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import (DictField, IntegerField, ListField,
                                        ModelSerializer, SerializerMethodField,
                                        SlugField)

from recipes.models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag
from users.models import ShoppingCart
from users.serializers import UserSerializer
from .nested import IngredientRecipeSerializer, TagSerializer

User = get_user_model()


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeListSerializer(ModelSerializer):
    tags = TagSerializer(many=True,)
    author = UserSerializer()
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('author', )

    def get_ingredients(self, object):
        queryset = IngredientRecipe.objects.filter(recipe=object)
        return IngredientRecipeSerializer(queryset, many=True).data

    def get_is_favorited(self, object):
        request = self.context['request']
        return (
            request.user.is_authenticated and
            Favorite.objects.filter(
                recipe=object, user=request.user
            ).exists()
        )

    def get_is_in_shopping_cart(self, object):
        request = self.context['request']
        return (
            request.user.is_authenticated and
            ShoppingCart.objects.filter(
                recipes=object, user=request.user
            ).exists()
        )


class RecipeWriteSerializer(ModelSerializer):
    ingredients = ListField(child=DictField(child=IntegerField()))
    tags = ListField(child=SlugField())
    image = Base64ImageField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'author',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def add_ingredients_and_tags(self, instance, ingredients, tags):
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=instance,
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                amount=ingredient['amount']
            )
        for tag in tags:
            instance.tags.add(get_object_or_404(Tag, id=int(tag)))
        return instance

    def create(self, validated_data):
        author = self.context['request'].user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        return self.add_ingredients_and_tags(recipe, ingredients, tags)

    def update(self, instance, validated_data):
        instance.tags.clear()
        instance.ingredients.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = self.add_ingredients_and_tags(instance, ingredients, tags)
        return super().update(instance, validated_data)


class FavoriteRecipeSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('recipe', 'user')
