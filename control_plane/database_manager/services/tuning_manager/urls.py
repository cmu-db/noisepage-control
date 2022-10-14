from django.urls import path
from . import views

urlpatterns = [
    path("tune_database_callback/", views.tune_database_callback, name="tune_database_callback"),
]
