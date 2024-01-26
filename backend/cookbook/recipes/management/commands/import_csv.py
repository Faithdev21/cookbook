from csv import DictReader

from django.core.management import BaseCommand
from django.db import IntegrityError

from recipes.models import Ingredient


class Command(BaseCommand):
    """Load CSV data into database"""
    def handle(self, *args, **kwargs):
        for row in DictReader(open('./data/ingredients.csv', encoding='utf-8')):
            try:
                ingredient = Ingredient(
                    name=row['name'],
                )
                ingredient.save()
            except IntegrityError:
                print("Ingredients with this name already created!")
        print("Ingredients ready!")
