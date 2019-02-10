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
