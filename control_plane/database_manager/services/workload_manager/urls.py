from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("collect_workload_callback/", views.collect_workload_callback, name="collect_workload_callback"),
    path("<str:workload_id>", views.download_workload),
]
