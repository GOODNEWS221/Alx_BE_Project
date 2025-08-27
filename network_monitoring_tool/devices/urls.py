from django.urls import path
from .views import (
    DeviceGroupListCreateView, DeviceGroupDetailView,
    NetworkDeviceListCreateView, NetworkDeviceDetailView
)
from . import views

urlpatterns = [
    # Device Groups
    path("groups/", DeviceGroupListCreateView.as_view(), name="device-group-list"),
    path("groups/<int:pk>/", DeviceGroupDetailView.as_view(), name="device-group-detail"),

    # Devices
    path("", NetworkDeviceListCreateView.as_view(), name="network-device-list"),
    path("<int:pk>/", NetworkDeviceDetailView.as_view(), name="network-device-detail"),

    path("groups/", views.device_group_list, name="device-group-list"),
    path("groups/add/", views.device_group_add, name="device-group-add"),
    path("groups/<int:pk>/edit/", views.device_group_edit, name="device-group-edit"),
    path("groups/<int:pk>/delete/", views.device_group_delete, name="device-group-delete"),

    # Network Devices
    path("", views.network_device_list, name="network-device-list"),
    path("add/", views.network_device_add, name="network-device-add"),
    path("<int:pk>/edit/", views.network_device_edit, name="network-device-edit"),
    path("<int:pk>/delete/", views.network_device_delete, name="network-device-delete"),
]
