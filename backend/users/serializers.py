from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from djoser.serializers import UserCreateSerializer
from recipes.serializers.nested import ShortRecipeSerializer
from rest_framework import serializers

from .models import Subscription

User = get_user_model()


class UserSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, object):
        request = self.context['request']
        return (
            request.user.is_authenticated and
            Subscription.objects.filter(
                author=object, user=request.user
            ).exists()
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserSubscriptionSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()
    recipes = ShortRecipeSerializer(many=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, object):
        request = self.context['request']
        return (
            request.user.is_authenticated and
            Subscription.objects.filter(
                author=object, user=request.user
            ).exists()
        )

    def get_recipes_count(self, objects):
        return objects.recipes.count()
