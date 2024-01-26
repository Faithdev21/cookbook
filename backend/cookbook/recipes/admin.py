from typing import Tuple

from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display: Tuple = ('name', 'amount',)
    search_fields: Tuple = ('name', 'amount',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines: Tuple = (RecipeIngredientInline,)
    list_filter: Tuple = ('id', 'name',)
    list_display: Tuple = ('id', 'name',)
    search_fields: Tuple = ('id', 'name',)
