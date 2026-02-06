from django.contrib import admin
from .models import Restaurant, FoodCategory, FoodItems

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(FoodCategory)
admin.site.register(FoodItems)