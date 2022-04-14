from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("healthcheck/", views.healthcheck, name="healthcheck"),
    path(
        "workload_capture_callback/",
        views.workload_capture_callback,
        name="workload_capture_callback",
    ),
]
