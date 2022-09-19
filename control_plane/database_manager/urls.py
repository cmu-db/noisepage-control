from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.list_databases, name="list_databases"),
    path("register/", views.register_database, name="register_database"),
    path(
        "workload/",
        include("database_manager.services.workload_manager.urls"),
    ),
]
