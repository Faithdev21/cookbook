from typing import Tuple, Type

from django.db import transaction
from django.db.models import OuterRef, Subquery, F
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api import constants
from api.mixins import ListCreateRetrieveDestroy
from api.serializers import (IngredientReadSerializer, RecipeCreateSerializer,
                             RecipeReadSerializer)
from recipes.models import Ingredient, Recipe, RecipeIngredient


class IngredientViewSet(ListCreateRetrieveDestroy):
    """Возвращает список ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientReadSerializer
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'patch', 'delete',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    http_method_names: Tuple[str, ...] = ('get', 'post', 'patch', 'delete',)
    ordering_fields: Tuple[str, ...] = ('id', 'name',)

    def get_serializer_class(self) -> Type:
        if self.action in constants.ACTION_METHODS:
            return RecipeCreateSerializer
        return RecipeReadSerializer

    @transaction.atomic
    @action(detail=False, methods=['GET'])
    def add_product_to_recipe(self, request):
        recipe_id = request.GET.get('recipe_id')
        product_id = request.GET.get('product_id')
        weight = request.GET.get('weight')

        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            ingredient = Ingredient.objects.get(pk=product_id)

            serializer = RecipeCreateSerializer(
                data={
                    'recipe': recipe_id,
                    'ingredient': product_id,
                    'weight': weight}
            )
            if serializer.is_valid():
                weight = serializer.validated_data['weight']

            recipe_ingredient, created = RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                defaults={'weight': weight}
            )

            if not created and recipe_ingredient.weight != weight:
                recipe_ingredient.weight = weight
                recipe_ingredient.save()

                return Response(
                    {'status': 'Вес продукта обновлен'},
                    status=status.HTTP_200_OK
                )

            return Response(
                {'status': 'Продукт добавлен'},
                status=status.HTTP_201_CREATED
            )

        except Recipe.DoesNotExist:
            return Response(
                {'error': 'Рецепт не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Ingredient.DoesNotExist:
            return Response(
                {'error': 'Продукт не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

    @transaction.atomic
    @action(detail=False, methods=['GET'])
    def cook_recipe(self, request):
        recipe_id = request.GET.get('recipe_id')
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe_ingredients = RecipeIngredient.objects.select_for_update().filter(recipe=recipe)

        updates = [
            Ingredient(
                id=recipe_ingredient.ingredient.id,
                amount=F('amount') + 1
            )
            for recipe_ingredient in recipe_ingredients
        ]
        Ingredient.objects.bulk_update(updates, ['amount'])

        return Response({'status': 'success'})

    @transaction.atomic
    @action(detail=False, methods=['GET'])
    def show_recipes_without_product(self, request):
        product_id = request.GET.getlist('product_id')

        recipes_without_product = Recipe.objects.exclude(
            id__in=Subquery(
                RecipeIngredient.objects.filter(
                    ingredient__id__in=product_id,
                    weight__gte=10,
                    recipe=OuterRef('pk')
                ).values('recipe')
            )
        )

        return render(
            request, 'recipes_without_product.html',
            {'recipes': recipes_without_product}
        )
