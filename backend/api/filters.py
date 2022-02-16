# from django_filters.rest_framework import (BooleanFilter, FilterSet,
#                                            ModelMultipleChoiceFilter)
# from rest_framework.filters import SearchFilter

# from recipes.models import Recipe, Tag


# class CustomSearchFilter(SearchFilter):
#     search_param = 'name'


# class RecipeFilter(FilterSet):
#     is_favorited = BooleanFilter(method='get_favorites')
#     is_in_shopping_list = BooleanFilter(method='get_in_shopping_list')
#     tags = ModelMultipleChoiceFilter(
#         field_name='tags_slug',
#         to_field_name='slug',
#         queryset=Tag.objects.all()
#     )

#     class Meta:
#         model = Recipe
#         fields = ('is_favorited', 'is_in_shopping_list', 'author', 'tags',)

#     def get_favorites(self, queryset, name, value):
#         if value:
#             return Recipe.objects.filter(
#                 favorited_by_user__user=self.request.user
#             )
#         return Recipe.objects.all()
