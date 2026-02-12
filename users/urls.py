from django.urls import path
from . import views

urlpatterns = [
    path("",views.auth_view, name = "auth"),
    path('logout/', views.logout_view, name = 'logout'),
    path('profile/', views.profile_view, name = 'profile'),
    path('search/', views.search, name='search'),


]
