from django.contrib import admin
from .models import PizzaBase, IngredientsCategory, Ingredients, Pizza

admin.site.register(PizzaBase)
admin.site.register(Ingredients)
admin.site.register(IngredientsCategory)
admin.site.register(Pizza)
