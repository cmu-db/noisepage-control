from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("collect_workload_callback/", views.collect_workload_callback, name="collect_workload_callback"),
    path("<str:database_id>", views.workloads), # TODO: Refactor to /databases (adhere to HTTP resources)
    path("download/<str:workload_id>", views.download_workload),
]
