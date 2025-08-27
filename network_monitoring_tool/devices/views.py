from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import DeviceGroup, NetworkDevice
from .serializers import DeviceGroupSerializer, NetworkDeviceSerializer
from users.permissions import IsAdmin, IsViewerOrReadOnly
from audit.models import AuditLog
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeviceGroupForm, NetworkDeviceForm


# Utility function for logging actions
def log_action(user, action, obj):
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=obj.__class__.__name__,
        object_id=obj.pk,
        changes=f"{action} {obj}"
    )


# -------------------
# Device Groups Views
# -------------------
class DeviceGroupListCreateView(generics.ListCreateAPIView):
    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer
    permission_classes = [IsViewerOrReadOnly]

    def perform_create(self, serializer):
        group = serializer.save()
        log_action(self.request.user, "CREATE", group)


class DeviceGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        group = serializer.save()
        log_action(self.request.user, "UPDATE", group)

    def perform_destroy(self, instance):
        log_action(self.request.user, "DELETE", instance)
        super().perform_destroy(instance)


# -------------------
# Network Devices Views
# -------------------
class NetworkDeviceListCreateView(generics.ListCreateAPIView):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer
    permission_classes = [IsViewerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "ip_address", "device_type", "location"]
    ordering_fields = ["added_at", "name"]
    ordering = ["-added_at"]

    def perform_create(self, serializer):
        device = serializer.save(added_by=self.request.user)
        log_action(self.request.user, "CREATE", device)


class NetworkDeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        device = serializer.save()
        log_action(self.request.user, "UPDATE", device)

    def perform_destroy(self, instance):
        log_action(self.request.user, "DELETE", instance)
        super().perform_destroy(instance)


def log_action(request, action, instance, details=""):
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        model_name=instance.__class__.__name__,
        object_id=str(instance.pk),
        details=details
    )



# --- Device Groups ---
def device_group_list(request):
    groups = DeviceGroup.objects.all()
    return render(request, "devices/device_group_list.html", {"groups": groups})

def device_group_add(request):
    if request.method == "POST":
        form = DeviceGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("device-group-list")
    else:
        form = DeviceGroupForm()
    return render(request, "devices/device_group_form.html", {"form": form, "form_title": "Add Device Group"})

def device_group_edit(request, pk):
    group = get_object_or_404(DeviceGroup, pk=pk)
    if request.method == "POST":
        form = DeviceGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect("device-group-list")
    else:
        form = DeviceGroupForm(instance=group)
    return render(request, "devices/device_group_form.html", {"form": form, "form_title": "Edit Device Group"})

def device_group_delete(request, pk):
    group = get_object_or_404(DeviceGroup, pk=pk)
    if request.method == "POST":
        group.delete()
        return redirect("device-group-list")
    return render(request, "devices/device_group_form.html", {"form": None, "form_title": "Delete Device Group"})

# --- Network Devices ---
def network_device_list(request):
    devices = NetworkDevice.objects.all()
    return render(request, "devices/network_device_list.html", {"devices": devices})

def network_device_add(request):
    if request.method == "POST":
        form = NetworkDeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.added_by = request.user
            device.save()
            return redirect("network-device-list")
    else:
        form = NetworkDeviceForm()
    return render(request, "devices/network_device_form.html", {"form": form, "form_title": "Add Network Device"})

def network_device_edit(request, pk):
    device = get_object_or_404(NetworkDevice, pk=pk)
    if request.method == "POST":
        form = NetworkDeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect("network-device-list")
    else:
        form = NetworkDeviceForm(instance=device)
    return render(request, "devices/network_device_form.html", {"form": form, "form_title": "Edit Network Device"})

def network_device_delete(request, pk):
    device = get_object_or_404(NetworkDevice, pk=pk)
    if request.method == "POST":
        device.delete()
        return redirect("network-device-list")
    return render(request, "devices/network_device_form.html", {"form": None, "form_title": "Delete Network Device"})