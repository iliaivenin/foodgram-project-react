# # from django.shortcuts import get_object_or_404
# # from djoser.views import UserViewSet
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import serializers, status, viewsets
# # from rest_framework.decorators import action
# from rest_framework.permissions import AllowAny, IsAuthenticated

# from recipes.models import (Favorite, Subscription, IngredientRecipe, Ingredient,
#                             Recipe, ShoppingCart, Tag, User)

# from .filters import CustomSearchFilter, RecipeFilter
# from .permissions import AuthorOrReadOnly
# from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer

# # from rest_framework.response import Response
# # from rest_framework.views import APIView


# class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     permission_classes = [AllowAny, ]
#     filter_backends = [CustomSearchFilter]
#     serch_fields = ['name', ]


# class TagViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = [AllowAny, ]


# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer
#     permission_classes = [AuthorOrReadOnly, ]
#     filter_backends = [DjangoFilterBackend]
#     filter_class = RecipeFilter
