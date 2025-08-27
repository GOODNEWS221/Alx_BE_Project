from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from metrics.models import NetworkDevice, DeviceMetric
from metrics.serializers import NetworkDeviceSerializer, DeviceMetricSerializer
from metrics.utils import ping_device   # import your ping helper
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import DeviceMetric

# 🔹 Device CRUD (Admin can add/remove, others can view)
class NetworkDeviceViewSet(viewsets.ModelViewSet):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 🔹 Custom endpoint: /api/devices/<id>/ping/
    @action(detail=True, methods=["get"], url_path="ping")
    def ping_test(self, request, pk=None):
        try:
            device = self.get_object()
            metric = ping_device(device)
            return Response({
                "device": device.name,
                "ip_address": device.ip_address,
                "ping_ms": metric.value,
                "timestamp": metric.timestamp
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# 🔹 List all metrics (with filtering)
class DeviceMetricListView(generics.ListAPIView):
    serializer_class = DeviceMetricSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = DeviceMetric.objects.all()

        # Filtering by device id
        device_id = self.request.query_params.get("device_id")
        if device_id:
            queryset = queryset.filter(device__id=device_id)

        # Filtering by metric type (ping, cpu, memory)
        metric_type = self.request.query_params.get("metric_type")
        if metric_type:
            queryset = queryset.filter(metric_type=metric_type)

        # Optional: date range filter
        start_time = self.request.query_params.get("start")
        end_time = self.request.query_params.get("end")
        if start_time and end_time:
            queryset = queryset.filter(timestamp__range=[start_time, end_time])

        return queryset.order_by("-timestamp")


# 🔹 Get latest metric for a device
class LatestDeviceMetricView(generics.RetrieveAPIView):
    serializer_class = DeviceMetricSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        device_id = kwargs.get("pk")
        metric = DeviceMetric.objects.filter(device__id=device_id).order_by("-timestamp").first()
        if metric:
            return Response(DeviceMetricSerializer(metric).data)
        return Response({"detail": "No metrics found for this device"}, status=404)


@login_required
def metrics_list(request):
    metrics_qs = DeviceMetric.objects.all().order_by("-timestamp")

    # Filters
    device_id = request.GET.get("device_id")
    metric_type = request.GET.get("metric_type")

    if device_id:
        metrics_qs = metrics_qs.filter(device__id=device_id)
    if metric_type:
        metrics_qs = metrics_qs.filter(metric_type=metric_type)

    # Pagination
    paginator = Paginator(metrics_qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "metrics/metrics_list.html", {"metrics": page_obj})
# Create your views here.

def metrics_list(request):
    # Start with all metrics
    metrics = DeviceMetric.objects.all().order_by('-timestamp')

    # Filter by device_id
    device_id = request.GET.get('device_id')
    if device_id:
        metrics = metrics.filter(device__id=device_id)

    # Filter by metric_type
    metric_type = request.GET.get('metric_type')
    if metric_type:
        metrics = metrics.filter(metric_type=metric_type)

    # Pagination: 25 per page
    paginator = Paginator(metrics, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass context including METRIC_TYPES for filter dropdown
    context = {
        "metrics": page_obj,
        "METRIC_TYPES": DeviceMetric.METRIC_TYPES,
    }

    return render(request, "metrics/metrics_list.html", context)
