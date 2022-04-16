from django.urls import path

from . import views
from exploratory_worker.services.exploratory_cluster_manager.views import (
    launch_exploratory_cluster,
    stop_exploratory_cluster,
)

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "launch_exploratory_cluster/",
        launch_exploratory_cluster,
        name="launch exploratory cluster",
    ),
    path(
        "stop_exploratory_cluster/",
        stop_exploratory_cluster,
        name="stop exploratory cluster",
    ),
]
