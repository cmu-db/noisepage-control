from django.urls import path
from . import views

urlpatterns = [
    path("apply/<str:tuning_action_id>", views.apply_action, name="apply_action"),
    path(
        "apply_action_callback/", 
        views.apply_action_callback, 
        name="apply_action_callback"),
]
