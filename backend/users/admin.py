from django.contrib import admin

from .models import CustomUser, ShoppingCart


@admin.register(CustomUser)
class User(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',)
    search_fields = ('email',)
    list_filter = ('email', 'username',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
