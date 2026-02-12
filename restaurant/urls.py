from django.urls import path 
from .import views 
from .views import home, restaurant_list


urlpatterns = [
    path('', views.home, name = 'home'),
    path("add/",views.add_res,name = 'add'),
    path("update/<int:id>/",views.update_res,name = "update_res"),
    path('delete/<int:id>/', views.delete_res, name="delete"),
    
    
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),

    path('category/<int:restaurant_id>/add-category/', views.add_category, name='add_category'),
    path("category/update/<int:id>/",views.update_category,name="update_category"),
    path("category/delete/<int:id>/",views.delete_category,name="delete_category"),

    path('food/<int:restaurant_id>/add-food/', views.add_food_item, name='add_food_item'),
    path('food/update/<int:id>/', views.update_food_item, name='update_food_item'),
    path('food/delete/<int:id>/', views.delete_food_item, name='delete_food_item'),
]

