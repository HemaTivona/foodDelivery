from .models import FoodCategory, FoodItems
from django import forms

class FoodCategoryForm(forms.ModelForm):
    class Meta:
        model = FoodCategory
        fields = ['name']

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItems
        fields = ['name', 'category', 'price', 'is_available']