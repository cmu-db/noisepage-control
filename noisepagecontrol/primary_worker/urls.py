from django.urls import path
from primary_worker.services.workload_manager.views import (
    start_workload_capture,
)

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("capture_workload/", start_workload_capture, name="start_workload_capture"),
]
