from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from recipes.models import Recipe
from recipes.permissions import AllowUnauthenticatedPost, IsAuthorOrReadOnlyPermission
from .models import Subscribe
from .pagination import CustomPagination
from users.serializers import RecipeShortSerializer, CustomUsersSerializer, SubscribeSerializer

User = get_user_model()


class CustomUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUsersSerializer
    #permission_classes = [AllowUnauthenticatedPost,]
    pagination_class = CustomPagination

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        """Подписаться отписаться от автора."""
        author = self.get_object()

        if request.method == 'POST':
            subscription, created = Subscribe.objects.get_or_create(
                user=request.user, author=author)
            if created:
                user_serializer = CustomUsersSerializer(
                    request.user, context={'request': request})
                recipes_serializer = RecipeShortSerializer(
                    Recipe.objects.filter(author=author), many=True)
                response_data = {
                    **user_serializer.data,
                    'is_subscribed': True,
                    'recipes': recipes_serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Already subscribed"}
                                , status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscribe, user=request.user, author=author)
            subscription.delete()
            user_serializer = CustomUsersSerializer(
                request.user, context={'request': request})
            response_data = {
                **user_serializer.data,
                'is_subscribed': False,
                'recipes': []
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        """Список подписок на авторов."""
        queryset = User.objects.filter(subscriber__user=request.user)
        serializer = SubscribeSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def user_recipes(self, request, pk=None):
        """Извлекать рецепты пользователя."""
        user = self.get_object()
        recipes = Recipe.objects.filter(author=user)
        recipe_serializer = RecipeShortSerializer(recipes, many=True)
        return Response(recipe_serializer.data)