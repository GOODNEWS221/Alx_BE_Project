"""
URL configuration for network_monitoring_tool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from devices.views import (
    DeviceGroupListCreateView, DeviceGroupDetailView,
    NetworkDeviceListCreateView, NetworkDeviceDetailView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import RegisterUserView, UserListView, UserDetailView, RoleListCreateView, RoleDetailView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("api/auth/register/", RegisterUserView.as_view(), name="register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Users
    path("api/users/", UserListView.as_view(), name="user-list"),
    path("api/users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),

    # Roles
    path("api/roles/", RoleListCreateView.as_view(), name="role-list"),
    path("api/roles/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),
]




urlpatterns += [
    # Device Groups
    path("api/device-groups/", DeviceGroupListCreateView.as_view(), name="device-group-list"),
    path("api/device-groups/<int:pk>/", DeviceGroupDetailView.as_view(), name="device-group-detail"),

    # Devices
    path("api/devices/", NetworkDeviceListCreateView.as_view(), name="device-list"),
    path("api/devices/<int:pk>/", NetworkDeviceDetailView.as_view(), name="device-detail"),
]
