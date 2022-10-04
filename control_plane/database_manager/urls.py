from django.urls import path, include

from . import views
from .services.state_manager import views as state_manager_views
# from services.workload_manager import views as workload_manager_views

urlpatterns = [
    path("databases/", views.list_databases, name="list_databases"),
    path("databases/<str:database_id>/", views.get_database, name="get_database"),
    path("databases/<str:database_id>/states", state_manager_views.states, name="states"),
    # path("databases/<str:database_id>/workloads/", workload_manager_views.workloads, name="workloads"),
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
