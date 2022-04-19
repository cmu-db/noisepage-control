from django.urls import path
from exploratory_worker.services.data_collector.views import collect_data
from exploratory_worker.services.exploratory_postgres_manager.views import (
    launch_exploratory_postgres,
    stop_exploratory_postgres,
)

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "launch_exploratory_postgres/",
        launch_exploratory_postgres,
        name="launch exploratory cluster",
    ),
    path(
        "stop_exploratory_postgres/",
        stop_exploratory_postgres,
        name="stop exploratory cluster",
    ),
    path(
        "collect_data/",
        collect_data,
        name="Collect data",
    ),
]
