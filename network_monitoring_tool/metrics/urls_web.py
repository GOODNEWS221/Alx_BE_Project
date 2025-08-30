from django.urls import path
from . import views

urlpatterns = [
    path("", views.metrics_list, name="metrics-list"),  # list metrics in table or summary
    path("add/", views.metric_add, name="metrics-add"),  # add new metric manually
    path("edit/<int:pk>/", views.metric_edit, name="metrics-edit"),  # edit a metric
    path("delete/<int:pk>/", views.metric_delete, name="metrics-delete"),  # delete a metric
    path("logs/", views.metrics_logs, name="metrics-logs"),  # visualization / availability graph
    path("metrics/logs/", views.metrics_logs, name="metrics-logs"),
    
]