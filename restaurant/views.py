from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Restaurant, FoodCategory, FoodItems
from django.http import HttpResponse, HttpResponseForbidden
from django import forms
from .form import FoodCategoryForm, FoodItemForm
from .decorators import admin_required
# Create your views here.

@login_required
def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'home.html', {
        'restaurants': restaurants
    })

@login_required
def add_res(request):
    # 🔒 Role-based protection
    if request.user.profile.role != "admin":
        return HttpResponseForbidden("You are not allowed to add restaurants")

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        rating = request.POST.get('rating')

        Restaurant.objects.create(
            name=name,
            description=description,
            rating=rating,
            owner=request.user
    )

        return redirect('home')

    return render(request, 'restaurant/res.html')



# @login_required
# def update_res(request,id):
#     rest = get_object_or_404(Restaurant,id = id, owner = request.user)
#     if request.method == 'POST':
#         rest.name = request.POST.get('name')
#         rest.description = request.POST.get('description')
#         rest.rating = request.POST.get('rating')
#         rest.save()
#         return redirect('home')
#     return render(request,'restaurant/res.html', {'rest': rest})

@login_required
def update_res(request, id):
    restaurant = get_object_or_404(Restaurant, id=id, owner=request.user)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.description = request.POST.get('description')
        restaurant.rating = request.POST.get('rating')
        restaurant.save()
        return redirect('home')

    return render(request, 'restaurant/res.html', {
        'restaurant': restaurant
    })
        
# @login_required
# def delete_res(request, id):
#     print("DELETE VIEW EXECUTED")
#     restaurant = get_object_or_404(Restaurant, id=id)
#     restaurant.delete()
#     return HttpResponse("DELETED SUCCESSFULLY")

@login_required
def delete_res(request, id):
    restaurant = get_object_or_404(
        Restaurant,
        id=id,
        owner=request.user
    )

    if request.method == "POST":
        restaurant.delete()
        return redirect("home")

    return redirect("home")

@login_required
@admin_required
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

    return render(request, 'category/add_category.html', {
        'form': form,
        'restaurant': restaurant
    })

@login_required
@admin_required
def update_category(request, id):
    category = get_object_or_404(FoodCategory, id=id)

    if request.method == "POST":
        form = FoodCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("restaurant_detail", category.restaurant.id)
    else:
        form = FoodCategoryForm(instance=category)

    return render(request, "category/add_category.html", {
        "form": form,
        "restaurant": category.restaurant,
        "category": category
    })

@login_required
@admin_required
def delete_category(request, id):
    category = get_object_or_404(FoodCategory, id=id)
    restaurant_id = category.restaurant.id

    if request.method == "POST":
        category.delete()
        return redirect("restaurant_detail", restaurant_id)

    return redirect("restaurant_detail", restaurant_id)


@login_required
@admin_required
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

    return render(request, 'food/add_food.html', {
        'form': form,
        'restaurant': restaurant
    })

@login_required
@admin_required
def update_food_item(request, id):
    food = get_object_or_404(FoodItems, id=id)
    restaurant = food.restaurant

    if request.method == "POST":
        form = FoodItemForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect("restaurant_detail", restaurant.id)
    else:
        form = FoodItemForm(instance=food)
        form.fields['category'].queryset = FoodCategory.objects.filter(
            restaurant=restaurant
        )

    return render(request, "food/add_food.html", {
        "form": form,
        "restaurant": restaurant,
        "food": food
    })


@login_required
@admin_required
def delete_food_item(request, id):
    food = get_object_or_404(FoodItems, id=id)
    restaurant_id = food.restaurant.id

    if request.method == "POST":
        food.delete()
        return redirect("restaurant_detail", restaurant_id)

    return redirect("restaurant_detail", restaurant_id)


def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    categories = restaurant.categories.all()

    return render(request, 'restaurant/res_detail.html', {
        'restaurant': restaurant,
        'categories': categories
    })

@login_required
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, "restaurant_list.html", {
        "restaurants": restaurants
    })
