from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Restaurant
from django.http import HttpResponse

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


    
