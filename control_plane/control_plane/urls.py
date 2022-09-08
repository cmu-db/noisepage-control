from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("debug/", include("control_plane.services.debug.urls")),
    path("database_manager/", include("database_manager.urls")),
]
