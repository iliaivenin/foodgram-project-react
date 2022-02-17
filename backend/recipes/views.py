from django.contrib.auth import get_user_model
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet

from recipes.serializers.base import (CreateRecipeSerializer,
                                      FavoriteRecipeSerializer,
                                      IngredientSerializer,
                                      RecipeListSerializer,
                                      RecipeWriteSerializer,
                                      TagSerializer)
from recipes.serializers.nested import ShortRecipeSerializer

from .filters import IngredientFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, Tag

from users.models import ShoppingCart

User = get_user_model()


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filterset_class = IngredientFilter


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class FavoriteRecipeViewSet(ModelViewSet):
    serializer_class = FavoriteRecipeSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        favorites = Favorite.objects.select_related(
            'recipe').filter(user=self.request.user)
        favorites_id = []
        for favorite in favorites:
            favorites_id.append(favorite.user.id)
        return Recipe.objects.filter(id__in=favorites_id)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = CreateRecipeSerializer
    serializer_class = RecipeListSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerializer
        # return CreateRecipeSerializer
        return RecipeWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeListSerializer(
            instance=serializer.instance,
            context={'request': self.request}
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=HTTP_201_CREATED, headers=headers
        )

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=partial
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     serializer = RecipeListSerializer(
    #         instance=serializer.instance,
    #         context={'request': self.request},
    #     )
    #     return Response(
    #         serializer.data, status=HTTP_200_OK
    #     )

    def get_favorite_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return ShortRecipeSerializer(*args, **kwargs)

    @action(methods=['get', 'delete'], detail=True)
    def favorite(self, request, id=None):
        recipe = get_object_or_404(Recipe, id=id)
        if self.request.method == 'DELETE':
            if Favorite.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                Favorite.objects.filter(
                    user=request.user, recipe=recipe
                ).delete()
                return Response(
                    {'info': 'Вы удалили рецепт из избранного'},
                    status=HTTP_204_NO_CONTENT
                )
            return Response(
                {'errors': 'Ошибка удаления из избранного'},
                status=HTTP_400_BAD_REQUEST
            )
        if Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            raise ValidationError({'info': 'Рецепт уже есть в избранном'})
        else:
            Favorite.objects.create(
                user=request.user, recipe=recipe
            )
        serializer = self.get_favorite_serializer(recipe)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(methods=['get', 'delete'], detail=True)
    def shopping_cart(self, request, id=None):
        recipe = get_object_or_404(Recipe, id=id)
        shopping_list = ShoppingCart.objects.get_or_create(
            user=request.user
        )[0]
        if self.request.method == 'GET':
            shopping_list.recipes.add(recipe)
        # serializer = self.get_favorite_serializer(recipe)
        # return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(status=HTTP_201_CREATED)
        shopping_list.recipes.remove(recipe)
        return Response(status=HTTP_204_NO_CONTENT)
