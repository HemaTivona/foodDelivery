from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Restaurant, FoodCategory, FoodItems
from django.http import HttpResponse
from django import forms
from .form import FoodCategoryForm, FoodItemForm

# Create your views here.

@login_required
def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'home.html', {
        'restaurants': restaurants
    })

@login_required
def add_res(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        rating = request.POST.get('rating')
        id = request.POST.get('id')

        Restaurant.objects.create(
            name = name,
            description = description,
            rating = rating,
            owner = request.user,
            )
        return redirect('home')

    return render(request, 'restaurant/res.html')


@login_required
def update_res(request,id):
    rest = get_object_or_404(Restaurant,id = id, owner = request.user)
    if request.method == 'POST':
        rest.name = request.POST.get('name')
        rest.description = request.POST.get('description')
        rest.rating = request.POST.get('rating')
        rest.save()
        return redirect('home')
    return render(request,'restaurant/res.html', {'rest': rest})
        
@login_required
def delete_res(request, id):
    print("DELETE VIEW EXECUTED")
    restaurant = get_object_or_404(Restaurant, id=id)
    restaurant.delete()
    return HttpResponse("DELETED SUCCESSFULLY")


    
@login_required
def add_category(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        form = FoodCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.restaurant = restaurant
            category.save()
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = FoodCategoryForm()

    return render(request, 'restaurant/add_category.html', {
        'form': form,
        'restaurant': restaurant
    })

@login_required
def add_food_item(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.restaurant = restaurant
            food.save()
            return redirect('restaurant_detail', restaurant.id)
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = FoodCategory.objects.filter(
            restaurant=restaurant
        )

    return render(request, 'restaurant/add_food.html', {
        'form': form,
        'restaurant': restaurant
    })

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    categories = restaurant.categories.all()

    return render(request, 'restaurant/res_detail.html', {
        'restaurant': restaurant,
        'categories': categories
    })