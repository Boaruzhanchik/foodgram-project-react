from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from .models import Recipe, RecipeIngredients
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from tags.models import Tag
from tags.serializers import TagSerializer
from ingredients.models import Ingredient
from users.serializers import CustomUsersSerializer

User = get_user_model()


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit')


class CreateUpdateRecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Количество ингредиента должно быть 1 или более.'
            ),
        )
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUsersSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients')
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart')

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.all()
        return RecipeIngredientsSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_anonymous:
            return obj.favorites.filter(user=user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return obj.in_shopping_cart.filter(id=user.id).exists()

    class Meta:
        model = Recipe
        fields = '__all__'


class CreateRecipeSerializer(serializers.ModelSerializer):
    author = CustomUsersSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = CreateUpdateRecipeIngredientsSerializer(many=True)
    image = Base64ImageField()
    name = serializers.CharField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(
        min_value=1
    )

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы один тег.'
            )

        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы один ингредиент.'
            )

        unique_ingredients = set()
        for item in value:
            ingredient_id = item['id']
            if ingredient_id in unique_ingredients:
                raise serializers.ValidationError(
                    'У рецепта не может быть два одинаковых ингредиента.'
                )
            unique_ingredients.add(ingredient_id)

        return value

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        for ingredient_data in ingredients:
            ingredient_id = ingredient_data['id']
            amount = ingredient_data['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient_id)

            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )

        return recipe

    class Meta:
        model = Recipe
        fields = '__all__'


class UpdateRecipeSerializer(serializers.ModelSerializer):
    author = CustomUsersSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = CreateUpdateRecipeIngredientsSerializer(many=True)
    image = Base64ImageField()
    name = serializers.CharField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(
        min_value=1
    )

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы один тег.'
            )

        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы один ингредиент.'
            )

        unique_ingredients = set()
        for item in value:
            ingredient_id = item['id']
            if ingredient_id in unique_ingredients:
                raise serializers.ValidationError(
                    'У рецепта не может быть два одинаковых ингредиента.'
                )
            unique_ingredients.add(ingredient_id)

        return value

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.tags.set(tags)
        instance.save()
        existing_ingredients = list(instance.ingredients.all())
        for ingredient_data in ingredients:
            ingredient_id = ingredient_data['id']
            amount = ingredient_data['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
            existing_ingredient = next(
                (i for i in existing_ingredients if i.ingredient == ingredient),
                None
            )

            if existing_ingredient:
                existing_ingredient.amount = amount
                existing_ingredient.save()
            else:

                RecipeIngredients.objects.create(
                    recipe=instance,
                    ingredient=ingredient,
                    amount=amount
                )

        return instance

    class Meta:
        model = Recipe
        fields = '__all__'