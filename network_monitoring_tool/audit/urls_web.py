from django.urls import path
from . import views

urlpatterns = [
    path("", views.audit_log_list, name="audit-list"),  # ✅ must match the template
]