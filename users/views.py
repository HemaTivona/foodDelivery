from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from restaurant.models import Restaurant,FoodCategory,FoodItems
from django.db.models import Q

def auth_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        # ---------- REGISTER ----------
        if action == "register":
            username = request.POST["username"]
            password = request.POST["password"]
            role = request.POST["role"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("auth")

            user = User.objects.create_user(
                username=username,
                password=password
            )

            # ⚠️ DO NOT create profile here
            # profile already exists via signal
            user.profile.role = role
            user.profile.save()

            login(request, user)
            return redirect("home")

        # ---------- LOGIN ----------
        if action == "login":
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials")

    return render(request, "users/auth.html")

def logout_view(request):
   logout(request)
   return redirect('auth')

@login_required
def profile_view(request):
    return render(request,'users/profile.html')

def search(request):
    query = request.GET.get('q', '')

    restaurants = []
    categories = []
    food_items = []

    if query:
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(rating__icontains=query)
        ).distinct()

        categories = FoodCategory.objects.filter(
            Q(name__icontains=query) |
            Q(restaurant__name__icontains=query)
        ).distinct()

        food_items = FoodItems.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(restaurant__name__icontains=query)
        ).distinct()

    return render(request, 'users/search.html', {
        'query': query,
        'restaurants': restaurants,
        'categories': categories,
        'food_items': food_items,
    })
