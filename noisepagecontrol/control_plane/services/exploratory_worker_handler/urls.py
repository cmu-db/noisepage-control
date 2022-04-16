from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("healthcheck/", views.healthcheck, name="healthcheck"),
    path(
        "launch_exploratory_cluster_callback/",
        views.launch_exploratory_cluster_callback,
        name="launch_exploratory_cluster_callback",
    ),
]
