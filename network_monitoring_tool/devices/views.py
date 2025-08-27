from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import DeviceGroup, NetworkDevice
from .serializers import DeviceGroupSerializer, NetworkDeviceSerializer
from users.permissions import IsAdmin, IsViewerOrReadOnly
from audit.models import AuditLog



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