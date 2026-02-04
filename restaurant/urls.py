from django.urls import path 
from .import views 
from .views import home

urlpatterns = [
    path('', views.home, name='home'),
    path("add/",views.add_res,name = 'add'),
    path("update/<int:id>/",views.update_res,name = "update_res"),
    path('delete/<int:id>/', views.delete_res, name="delete_res")
    
    ]
