from django.contrib import admin
from users.models import Subscription

from .models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag


class IngredientRecipeInLine(admin.TabularInline):
    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'pub_date', 'author', 'name', 'text',)
    search_fields = ('text',)
    list_filter = ('pub_date', 'name', 'author',)
    empty_value_display = '-пусто-'
    inlines = [IngredientRecipeInLine]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(IngredientRecipe)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
