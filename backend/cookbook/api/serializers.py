from typing import Dict, Tuple

from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from recipes.models import Ingredient, Recipe, RecipeIngredient


class IngredientReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра ингредиентов."""

    class Meta:
        model = Ingredient
        fields: Tuple[str, ...] = ('id', 'name', 'amount')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для поля ingredients."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = RecipeIngredient
        fields: Tuple[str, ...] = ('id', 'name', 'weight',)


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецептов."""
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipe_ingredients'
    )

    class Meta:
        model = Recipe
        fields: Tuple[str, ...] = ('id', 'name', 'ingredients')

    def to_representation(self, instance: object) -> object:
        """Возвращает представление объекта рецепта
        через RecipeReadSerializer сериализатор."""
        representation = super().to_representation(instance)
        for ingredient_data in representation['ingredients']:
            ingredient_data['weight'] = f"{ingredient_data['weight']}г"
        return representation


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецептов."""
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields: Tuple[str, ...] = ('id', 'name', 'ingredients')

    def validate(self, data: Dict) -> Dict:
        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError("Ingredients field is required.")

        for ingredient_data in ingredients:
            weight = ingredient_data.get('weight')

            if weight is None:
                raise serializers.ValidationError(
                    "Weight field is required."
                )
            if weight < 1:
                raise serializers.ValidationError(
                    "Weight field must be more then 0."
                )

        return data

    def create(self, validated_data: Dict) -> ReturnDict:
        """Создает и возвращает объект рецепта."""
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)

        recipe_ingredients = [
            RecipeIngredient(
                recipe=instance,
                ingredient=ingredient_data.get('ingredient'),
                weight=ingredient_data.get('weight')
            )
            for ingredient_data in ingredients
        ]
        instance.recipe_ingredients.bulk_create(recipe_ingredients)
        return instance

    def to_representation(self, instance: object) -> object:
        """Возвращает представление объекта рецепта
        через RecipeReadSerializer сериализатор."""
        return RecipeReadSerializer(instance).data
