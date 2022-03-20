from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST)

from .models import Subscription
from .serializers import UserSubscriptionSerializer

User = get_user_model()


class UserSubscriptionViewSet(UserViewSet):
    pagination_class = PageNumberPagination
    lookup_url_kwarg = 'id'

    def get_subscription_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return UserSubscriptionSerializer(*args, **kwargs)

    @action(detail=False)
    def subscriptions(self, request):
        subscriptions = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset=subscriptions)
        if page is not None:
            serializer = self.get_subscription_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_subscription_serializer(subscriptions, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get', 'delete'], detail=True)
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        if self.request.method == 'DELETE':
            if Subscription.objects.filter(
                user=request.user, author=author
            ).exists():
                Subscription.objects.filter(
                    user=request.user, author=author
                ).delete()
                return Response(
                    {'info': 'Вы отписались от пользователя'},
                    status=HTTP_204_NO_CONTENT
                )
            return Response(
                {'errors': 'Ошибка отписки'}, status=HTTP_400_BAD_REQUEST
            )
        if Subscription.objects.filter(
            user=request.user, author=author
        ).exists():
            raise ValidationError({'info': 'Подписка уже существует'})
        else:
            Subscription.objects.create(
                user=request.user, author=author)
        serializer = self.get_subscription_serializer(author)
        return Response(serializer.data, status=HTTP_201_CREATED)
