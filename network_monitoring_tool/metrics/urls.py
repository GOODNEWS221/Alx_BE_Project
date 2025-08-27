from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import metrics_list
from . import views
from metrics.views import NetworkDeviceViewSet, DeviceMetricListView, LatestDeviceMetricView

router = DefaultRouter()
router.register(r"devices", NetworkDeviceViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("metrics/", DeviceMetricListView.as_view(), name="metrics-list"),
    path("metrics/latest/<int:pk>/", LatestDeviceMetricView.as_view(), name="metrics-latest"),
    path("logs/", metrics_list, name="metrics-list-ui"),
    path("logs/", views.metrics_list, name="metrics-list"),
]



