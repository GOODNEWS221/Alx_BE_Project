from django.urls import path
from . import views

urlpatterns = [
    path("", views.metrics_list, name="metrics-list"),       # list page
    path("add/", views.metric_add, name="metrics-add"),      # add metric
    path("edit/<int:pk>/", views.metric_edit, name="metrics-edit"),  # edit metric
    path("delete/<int:pk>/", views.metric_delete, name="metrics-delete"),  # delete metric
]

