from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import DeviceGroup, NetworkDevice
from .serializers import DeviceGroupSerializer, NetworkDeviceSerializer
from users.permissions import IsAdmin, IsViewerOrReadOnly

# Device Groups
class DeviceGroupListCreateView(generics.ListCreateAPIView):
    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer
    permission_classes = [IsViewerOrReadOnly]


class DeviceGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer
    permission_classes = [IsAdmin]


# Network Devices
class NetworkDeviceListCreateView(generics.ListCreateAPIView):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer
    permission_classes = [IsViewerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class NetworkDeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer
    permission_classes = [IsAdmin]


