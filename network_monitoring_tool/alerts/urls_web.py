from django.urls import path
from . import views

urlpatterns = [
    path("", views.alert_list, name="alerts-list"),  # matches your template URL tag
    # You can add more web views like add/edit/delete if needed
]
