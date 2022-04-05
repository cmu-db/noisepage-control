from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("launch_exploratory_cluster", views.launch_exploratory_cluster, name="launch exploratory cluster"),
    path("collect_training_data", views.collect_training_data, name="collect training data"),
    path("stop_exploratory_cluster", views.stop_exploratory_cluster, name="stop exploratory cluster")
]
