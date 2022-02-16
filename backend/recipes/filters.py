from django_filters import (
    AllValuesMultipleFilter,
    BooleanFilter,
    CharFilter,
    FilterSet,
)

from .models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart'
    )
    tags = AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['author']

    def get_is_favorited(self, queryset, name, value):
        if not value:
            return queryset
        favorites = self.request.user.favorites.all()
        return queryset.filter(
            pk__in=(favorite.recipe.pk for favorite in favorites)
        )

    def get_is_in_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        recipes = self.request.user.shopping_cart.recipes.all()
        return queryset.filter(
            pk__in=(recipe.pk for recipe in recipes)
        )
