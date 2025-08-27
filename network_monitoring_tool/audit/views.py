from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all().order_by("-timestamp")
    serializer_class = AuditLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Exact filters
    filterset_fields = ["user", "action", "model_name"]

    # Search inside details
    search_fields = ["details"]

    # Sort by timestamp
    ordering_fields = ["timestamp"]
