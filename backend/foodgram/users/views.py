from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from recipes.models import Recipe
from recipes.permissions import (AllowUnauthenticatedPost,
                                 IsAuthorOrReadOnlyPermission)
from .models import Subscribe
from .pagination import CustomPagination
from users.serializers import RecipeShortSerializer, CustomUsersSerializer, SubscribeSerializer, CustomUsersCreateSerializer

User = get_user_model()


class CustomUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUsersCreateSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        user = request.user
        current_password = request.data.get('current_password', None)
        new_password = request.data.get('new_password', None)

        if not current_password or not new_password:
            return Response({'detail': 'current_password and new_password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({'detail': 'Incorrect current password.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    #@action(detail=False, methods=['post'])
    #def set_password(self, request):
    #    user = request.user
    #    current_password = request.data.get('current_password', None)
    #    new_password = request.data.get('new_password', None)
#
    #    if not current_password or not new_password:
    #        return Response({'detail': 'current_password and new_password are required.'}, status=400)
#
    #    if not user.check_password(current_password):
    #        return Response({'detail': 'Incorrect current password.'}, status=400)
#
    #    user.set_password(new_password)
    #    user.save()
    #    return Response({'detail': 'Password changed successfully.'}, status=200)
#
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = CustomUsersSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        """Подписаться или отписаться от автора."""
        author = self.get_object()

        if request.method == 'POST':
            subscription, created = Subscribe.objects.get_or_create(
                user=request.user, author=author)
            if created:
                user_serializer = CustomUsersSerializer(
                    author, context={'request': request})
                recipes_serializer = RecipeShortSerializer(
                    Recipe.objects.filter(author=author), many=True)
                recipes_count = Recipe.objects.filter(author=author).count()
                response_data = {
                    **user_serializer.data,
                    'is_subscribed': True,
                    'recipes': recipes_serializer.data,
                    'recipes_count': recipes_count
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Already subscribed"}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscribe, user=request.user, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscribe.objects.filter(user=user)
        authors = [subscription.author for subscription in subscriptions]

        data = []
        for author in authors:
            user_serializer = CustomUsersSerializer(author, context={'request': request})
            recipes_serializer = RecipeShortSerializer(Recipe.objects.filter(author=author), many=True)
            recipes_count = Recipe.objects.filter(author=author).count()
            response_data = {
                **user_serializer.data,
                'recipes': recipes_serializer.data,
                'recipes_count': recipes_count
            }
            data.append(response_data)

        return Response(data)

    @action(detail=True, methods=['get'])
    def user_recipes(self, request, pk=None):
        """Извлекать рецепты пользователя."""
        user = self.get_object()
        recipes = Recipe.objects.filter(author=user)
        recipe_serializer = RecipeShortSerializer(recipes, many=True)
        return Response(recipe_serializer.data)