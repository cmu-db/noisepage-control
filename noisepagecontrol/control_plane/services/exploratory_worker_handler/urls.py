from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("healthcheck/", views.healthcheck, name="healthcheck"),
    path(
        "launch_exploratory_postgres_callback/",
        views.launch_exploratory_postgres_callback,
        name="launch_exploratory_postgres_callback",
    ),
    path(
        "data_collector_callback/",
        views.data_collector_callback,
        name="data_collector_callback",
    ),
]
