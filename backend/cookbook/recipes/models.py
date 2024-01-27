from django.core.validators import MinValueValidator
from django.db import models

from recipes.validators import validate_number


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name='Название ингредиента',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество использований в рецептах',
        validators=[validate_number],
        default=0,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        db_index=True,
        null=False,
        unique=True,
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингридиент',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pk',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель, связывающая рецепты и ингредиенты."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    weight = models.PositiveSmallIntegerField(
        verbose_name='Вес',
        null=False,
        validators=[validate_number, MinValueValidator(limit_value=1)],
    )

    class Meta:
        verbose_name = 'вес ингредиента в грамма'
        verbose_name_plural = 'вес ингредиентов в граммах'
        ordering = ('-recipe__pk',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} - {self.weight}г'
