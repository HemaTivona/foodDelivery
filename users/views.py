from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from restaurant.models import Restaurant
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


from django.http import JsonResponse
from django.db.models import Q


def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(rating__icontains=query) |
            Q(categories__name__icontains=query) |   # ✅ FIXED
            Q(fooditems__name__icontains=query)       # ✅ FIXED
        ).distinct()

        results = restaurants.values(
            'id',
            'name',
            'rating'
        )

    return JsonResponse({'results': list(results)})
