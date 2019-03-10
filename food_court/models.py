from django.db import models


class PizzaBase(models.Model):
    base_name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.base_name


class IngredientsCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    ingredients_category = models.ForeignKey(IngredientsCategory, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    pizza_name = models.CharField(max_length=100)
    description = models.TextField(('description'), blank=True)
    pizza_base = models.ForeignKey(PizzaBase, on_delete=models.PROTECT)
    ingredients = models.ManyToManyField(Ingredients)

    def __str__(self):
        return self.pizza_name
