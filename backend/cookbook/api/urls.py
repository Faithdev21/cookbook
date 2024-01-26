from django.urls import include, path
from rest_framework import routers

from api.views import IngredientViewSet, RecipeViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('add_product_to_recipe/', RecipeViewSet.as_view(
        {'get': 'add_product_to_recipe'})),
    path('show_recipes_without_product/', RecipeViewSet.as_view(
        {'get': 'show_recipes_without_product'})),
    path('cook_recipe/', RecipeViewSet.as_view(
        {'get': 'cook_recipe'})),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
]
