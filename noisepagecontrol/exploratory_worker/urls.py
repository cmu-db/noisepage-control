from django.urls import path

from . import views
from exploratory_worker.services.exploratory_postgres_manager.views import (
    launch_exploratory_postgres,
    stop_exploratory_postgres,
)

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
]
