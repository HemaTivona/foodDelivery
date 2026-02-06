from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    rating =models.FloatField(default = 1.0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


def __str__(self):
    return self.name

class FoodCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)

def __str__(self):
    return f" {self.name} - {self.restaurant.name}"

class FoodItems(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='fooditems')
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

def __str__(self):
    return self.name

