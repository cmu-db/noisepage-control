from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tune", views.tune_database, name="tune_database"),
]
