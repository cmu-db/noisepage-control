from django.urls import path

from . import views
from primary_worker.services.workload_manager.views import start_workload_capture

urlpatterns = [
    path("", views.index, name="index"),
    path("capture_workload/", start_workload_capture, name="start_workload_capture"),
]
