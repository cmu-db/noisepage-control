from django.urls import path
from . import views

urlpatterns = [
    path("generate_action_callback/", views.generate_action_callback, name="generate_action_callback"),
    path("<str:action_id>", views.download_action),
]
