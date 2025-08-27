from django.urls import path
from .views import (
    DeviceGroupListCreateView, DeviceGroupDetailView,
    NetworkDeviceListCreateView, NetworkDeviceDetailView
)

urlpatterns = [
    # Device Groups
    path("groups/", DeviceGroupListCreateView.as_view(), name="device-group-list"),
    path("groups/<int:pk>/", DeviceGroupDetailView.as_view(), name="device-group-detail"),

    # Devices
    path("", NetworkDeviceListCreateView.as_view(), name="network-device-list"),
    path("<int:pk>/", NetworkDeviceDetailView.as_view(), name="network-device-detail"),
]
