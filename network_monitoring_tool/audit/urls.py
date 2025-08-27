from django.urls import path
from .views import AuditLogListView
from . import views

urlpatterns = [
    path("", AuditLogListView.as_view(), name="audit-log-list"),
    path("logs/", AuditLogListView.as_view(), name="audit-logs"),

    # API
    path("api/", views.AuditLogListView.as_view(), name="audit-log-api"),

    # Template/UI
    path("", views.audit_log_list, name="audit-log-list"),
]