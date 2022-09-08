from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_databases, name="list_databases"),
    path("register/", views.register_database, name="register_database"),
]
