from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditLog
from .serializers import AuditLogSerializer

# REST API view
class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all().order_by("-timestamp")
    serializer_class = AuditLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["user", "action", "model_name"]
    search_fields = ["details"]
    ordering_fields = ["timestamp"]

# Template / UI view
@login_required
def audit_log_list(request):
    logs = AuditLog.objects.all().order_by("-timestamp")
    paginator = Paginator(logs, 25)  # 25 logs per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "audit/audit_log_list.html", {"logs": page_obj})
