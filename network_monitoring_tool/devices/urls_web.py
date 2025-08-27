from django.urls import path
from . import views

urlpatterns = [
    # Device Groups
    path("groups/", views.device_group_list, name="device-group-list"),
    path("groups/add/", views.device_group_add, name="device-group-add"),
    path("groups/edit/<int:pk>/", views.device_group_edit, name="device-group-edit"),
    path("groups/delete/<int:pk>/", views.device_group_delete, name="device-group-delete"),

    # Network Devices
    path("", views.network_device_list, name="network-device-list"),
    path("add/", views.network_device_add, name="network-device-add"),
    path("edit/<int:pk>/", views.network_device_edit, name="network-device-edit"),
    path("delete/<int:pk>/", views.network_device_delete, name="network-device-delete"),
]
