from django.urls import path 
from .import views 
from .views import home

urlpatterns = [
    path('', views.home, name = 'home'),
    path("add/",views.add_res,name = 'add'),
    path("update/<int:id>/",views.update_res,name = "update_res"),
    path('delete/<int:id>/', views.delete_res, name="delete_res"),
    path('restaurant/<int:restaurant_id>/add-category/', views.add_category, name='add_category'),
    path('restaurant/<int:restaurant_id>/add-food/', views.add_food_item, name='add_food_item'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
]