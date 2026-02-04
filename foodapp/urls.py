from django.urls import path
from .import views

urlpatterns = [
    path("home/",views.home_view, name = "home"),
    path("about/",views.about, name = "about"),
    path("contact/",views.contact, name = "contact"),
]
