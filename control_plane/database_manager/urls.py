from django.urls import path, include

from . import views
from .services.state_manager import views as state_manager_views
from .services.workload_manager import views as workload_manager_views
from .services.tuning_manager import views as tuning_manager_views
from .services.action_manager import views as action_manager_views

urlpatterns = [
    path("databases/", views.list_databases, name="list_databases"),
    path("databases/<str:database_id>/", views.get_database, name="get_database"),
    path("databases/<str:database_id>/states", state_manager_views.states, name="states"),
    path("databases/<str:database_id>/workloads", workload_manager_views.workloads, name="workloads"),
    path("databases/<str:database_id>/tune", tuning_manager_views.tune, name="tune"),
    path("databases/<str:database_id>/actions", action_manager_views.get_actions, name="get_actions"),
    path("register/", views.register_database, name="register_database"),
    path(
        "workload/",
        include("database_manager.services.workload_manager.urls"),
    ),
    path(
        "state/",
        include("database_manager.services.state_manager.urls"),
    ),
    path(
        "tune/",
        include("database_manager.services.tuning_manager.urls"),
    ),
    path(
        "action/",
        include("database_manager.services.action_manager.urls"),
    ),
]
