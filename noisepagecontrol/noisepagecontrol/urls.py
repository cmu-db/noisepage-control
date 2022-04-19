from constants import (
    SERVER_MODE_CONTROL_PLANE,
    SERVER_MODE_EXPLORATORY_WORKER,
    SERVER_MODE_PRIMARY_WORKER,
)
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = []

SERVER_MODE = settings.SERVER_MODE

"""
    Setup admin URLs only on CONTROL_PLANE
"""
if SERVER_MODE == SERVER_MODE_CONTROL_PLANE:
    urlpatterns += [
        path("admin/", admin.site.urls),
    ]

"""
    Include URLs based on the server mode
"""
if SERVER_MODE == SERVER_MODE_CONTROL_PLANE:
    urlpatterns += [
        path("", include("control_plane.urls")),
    ]
elif SERVER_MODE == SERVER_MODE_PRIMARY_WORKER:
    urlpatterns += [
        path("", include("primary_worker.urls")),
    ]
elif SERVER_MODE == SERVER_MODE_EXPLORATORY_WORKER:
    urlpatterns += [
        path("", include("exploratory_worker.urls")),
    ]
