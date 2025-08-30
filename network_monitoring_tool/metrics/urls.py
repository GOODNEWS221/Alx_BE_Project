from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NetworkDeviceViewSet,
    DeviceMetricListView,
    LatestDeviceMetricView,
    metrics_list,  # UI view
)

router = DefaultRouter()
router.register(r"devices", NetworkDeviceViewSet)

urlpatterns = [
    # API routes
    path("", include(router.urls)),
    path("metrics/", DeviceMetricListView.as_view(), name="metrics-list"),
    path("metrics/latest/<int:pk>/", LatestDeviceMetricView.as_view(), name="metrics-latest"),

    # UI route for metrics visualization/logs
    path("logs/", metrics_list, name="metrics-logs"),
]
