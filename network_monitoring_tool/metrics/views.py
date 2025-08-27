from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from metrics.models import NetworkDevice, DeviceMetric
from metrics.serializers import NetworkDeviceSerializer, DeviceMetricSerializer
from metrics.utils import ping_device   # import your ping helper


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
        return Response({"detail": "No metrics found for this device"}, status=404)r

# Create your views here.
