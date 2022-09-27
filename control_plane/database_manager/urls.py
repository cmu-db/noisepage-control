from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.list_databases, name="list_databases"),
    path("<str:database_id>/", views.get_database, name="get_database"),
    path("register/", views.register_database, name="register_database"),
    path(
        "workload/",
        include("database_manager.services.workload_manager.urls"),
    ),
    path(
        "state/",
        include("database_manager.services.state_manager.urls"),
    ),
]
