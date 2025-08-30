from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.http import JsonResponse

from .models import NetworkDevice, DeviceMetric
from .serializers import NetworkDeviceSerializer, DeviceMetricSerializer
from .forms import DeviceMetricForm
from .utils import ping_device  # your ping helper


# --------------------------
# API Views (DRF)
# --------------------------

class NetworkDeviceViewSet(viewsets.ModelViewSet):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class DeviceMetricListView(generics.ListAPIView):
    serializer_class = DeviceMetricSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = DeviceMetric.objects.all()
        device_id = self.request.query_params.get("device_id")
        metric_type = self.request.query_params.get("metric_type")
        start_time = self.request.query_params.get("start")
        end_time = self.request.query_params.get("end")

        if device_id:
            queryset = queryset.filter(device__id=device_id)
        if metric_type:
            queryset = queryset.filter(metric_type=metric_type)
        if start_time and end_time:
            queryset = queryset.filter(timestamp__range=[start_time, end_time])
        return queryset.order_by("-timestamp")


class LatestDeviceMetricView(generics.RetrieveAPIView):
    serializer_class = DeviceMetricSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        device_id = kwargs.get("pk")
        metric = DeviceMetric.objects.filter(device__id=device_id).order_by("-timestamp").first()
        if metric:
            return Response(DeviceMetricSerializer(metric).data)
        return Response({"detail": "No metrics found for this device"}, status=404)


# --------------------------
# Web Views
# --------------------------

@login_required
def metrics_list(request):
    metrics = DeviceMetric.objects.all().order_by('-timestamp')

    # Filters
    device_id = request.GET.get('device_id')
    metric_type = request.GET.get('metric_type')
    if device_id:
        metrics = metrics.filter(device__id=device_id)
    if metric_type:
        metrics = metrics.filter(metric_type=metric_type)

    # Pagination
    paginator = Paginator(metrics, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Build query params for pagination links
    query_params = ""
    if device_id:
        query_params += f"&device_id={device_id}"
    if metric_type:
        query_params += f"&metric_type={metric_type}"

    context = {
        "metrics": page_obj,
        "METRIC_TYPES": DeviceMetric.METRIC_TYPES,
        "query_params": query_params,  # pass to template
    }
    return render(request, "metrics/metrics_list.html", context)


@login_required
def metric_add(request):
    if request.method == "POST":
        form = DeviceMetricForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("metric-list")
    else:
        form = DeviceMetricForm()
    return render(request, "metrics/metric_form.html", {"form": form, "form_title": "Add Metric"})


@login_required
def metric_edit(request, pk):
    metric = get_object_or_404(DeviceMetric, pk=pk)
    if request.method == "POST":
        form = DeviceMetricForm(request.POST, instance=metric)
        if form.is_valid():
            form.save()
            return redirect("metric-list")
    else:
        form = DeviceMetricForm(instance=metric)
    return render(request, "metrics/metric_form.html", {"form": form, "form_title": "Edit Metric"})


@login_required
def metric_delete(request, pk):
    metric = get_object_or_404(DeviceMetric, pk=pk)
    if request.method == "POST":
        metric.delete()
        return redirect("metric-list")
    return render(request, "metrics/metric_form.html", {"form": None, "form_title": "Delete Metric"})


# --------------------------
# Visualization (Graph Views)
# --------------------------

@login_required
def metrics_logs(request):
    """ Page that will render the chart """
    devices = NetworkDevice.objects.all()
    return render(request, "metrics/metrics_logs.html", {"devices": devices})


@login_required
def metrics_data(request, device_id):
    """
    Endpoint returning JSON data for chart.js
    Example: /metrics/data/1/ (fetch last 50 ping/availability records)
    """
    metrics = DeviceMetric.objects.filter(device_id=device_id, metric_type="ping").order_by("-timestamp")[:50]
    data = {
        "labels": [m.timestamp.strftime("%H:%M:%S") for m in metrics[::-1]],
        "values": [m.value for m in metrics[::-1]],
    }
    return JsonResponse(data)
