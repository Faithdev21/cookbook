from typing import Tuple, Type

from django.db import transaction
from django.db.models import Q, Sum
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
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
    ordering_fields: Tuple[str, ...] = ('name',)

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
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ingredients = recipe.recipe_ingredients.all()

        for ingredient in ingredients:
            ingredient.ingredient.amount += 1
            ingredient.ingredient.save()

        return Response({'status': 'success'})

    @transaction.atomic
    @action(detail=False, methods=['GET'])
    def show_recipes_without_product(self, request):
        product_id = request.GET.get('product_id')

        recipes_without_product = Recipe.objects.filter(
            ~Q(recipe_ingredients__ingredient_id=product_id)
            | Q(recipe_ingredients__weight__lt=10)
        ).annotate(total_weight=Sum('recipe_ingredients__weight'))

        return render(
            request, 'recipes_without_product.html',
            {'recipes': recipes_without_product}
        )
