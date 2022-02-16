from django.contrib.auth import get_user_model
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework.generics import get_object_or_404
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import (DictField, IntegerField, ListField,
                                        ModelSerializer,
                                        SerializerMethodField, SlugField,
                                        ValidationError)

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Tag)
from users.serializers import UserSerializer
from users.models import ShoppingCart

from .nested import (AddIngredientToRecipeSerializer,
                     IngredientRecipeSerializer, TagSerializer)

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
    # ingredients = AddIngredientToRecipeSerializer(many=True)
    ingredients = ListField(child=DictField(child=IntegerField()))
    tags = ListField(child=SlugField())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context['request'].user
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                amount=ingredient['amount']
            )
        for tag in tags:
            recipe.tags.add(get_object_or_404(Tag, id=int(tag)))

        return recipe

# class AddIngredientToRecipeSerializer(ModelSerializer):
#     id = IntegerField()
#     amount = IntegerField()

#     class Meta:
#         model = Ingredient
#         fields = ('id', 'amount')


class CreateRecipeSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = AddIngredientToRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('recipe', 'user')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        for ingredient in ingredients:
            if Ingredient['amount'] <= 0:
                raise ValidationError(
                    'Количество ингредиента не может быть '
                    'отрицательным числом или нулём'
                )
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            object = get_object_or_404(Ingredient, id=ingredient['id'])
            amount = ingredient['amount']
            if IngredientRecipe.objects.filter(
                recipe=recipe,
                ingredient=object
            ).exists():
                amount += F('amount')
            IngredientRecipe.objects.update_or_create(
                recipe=recipe,
                ingredient=object,
                defaults={'amount': amount}
            )
        return recipe


class FavoriteRecipeSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('recipe', 'user')
