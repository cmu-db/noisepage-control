from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("debug/", include("control_plane.services.debug.urls")),
    path("tuning_manager/", include("control_plane.services.tuning_manager.urls")),
    path(
        "primary_worker_handler/",
        include("control_plane.services.primary_worker_handler.urls"),
    ),
    path(
        "exploratory_worker_handler/",
        include("control_plane.services.exploratory_worker_handler.urls"),
    ),
]
