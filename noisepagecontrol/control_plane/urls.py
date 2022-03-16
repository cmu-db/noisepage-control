from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("debug/", include("control_plane.services.debug.urls")),
    path("tuningmanager/", include("control_plane.services.tuning_manager.urls")),
]
