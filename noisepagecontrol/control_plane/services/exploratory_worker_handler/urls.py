from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("healthcheck/", views.healthcheck, name="healthcheck"),
]
