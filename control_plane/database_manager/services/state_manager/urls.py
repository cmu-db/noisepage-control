from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("collect_state_callback/", views.collect_state_callback, name="collect_state_callback"),
    path("<str:state_id>", views.download_state),
]
