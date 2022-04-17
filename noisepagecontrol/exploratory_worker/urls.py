from django.urls import path

from . import views
from exploratory_worker.services.exploratory_cluster_manager.views import (
    launch_exploratory_cluster,
    stop_exploratory_cluster,
)
from exploratory_worker.services.data_collector.views import (
    collect_data,
)

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "launch_exploratory_cluster",
        launch_exploratory_cluster,
        name="launch exploratory cluster",
    ),
    path(
        "stop_exploratory_cluster",
        stop_exploratory_cluster,
        name="stop exploratory cluster",
    ),
    path(
        "collect_data/",
        collect_data,
        name="Collect data",
    ),
]
