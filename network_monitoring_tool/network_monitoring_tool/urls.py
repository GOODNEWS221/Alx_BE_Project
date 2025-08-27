from django.contrib import admin
from django.urls import include, path
from devices.views import (
    DeviceGroupListCreateView, DeviceGroupDetailView,
    NetworkDeviceListCreateView, NetworkDeviceDetailView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("api/auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Users app routes (register, users, roles, etc.)
    path("api/users/", include("users.urls")),

    # Devices
    path("api/devices/groups/", DeviceGroupListCreateView.as_view(), name="device-group-list"),
    path("api/devices/groups/<int:pk>/", DeviceGroupDetailView.as_view(), name="device-group-detail"),
    path("api/devices/", NetworkDeviceListCreateView.as_view(), name="network-device-list"),
    path("api/devices/<int:pk>/", NetworkDeviceDetailView.as_view(), name="network-device-detail"),
]




urlpatterns += [
    # Device Groups
    path("api/device-groups/", DeviceGroupListCreateView.as_view(), name="device-group-list"),
    path("api/device-groups/<int:pk>/", DeviceGroupDetailView.as_view(), name="device-group-detail"),

    # Devices
    path("api/devices/", NetworkDeviceListCreateView.as_view(), name="device-list"),
    path("api/devices/<int:pk>/", NetworkDeviceDetailView.as_view(), name="device-detail"),
]
