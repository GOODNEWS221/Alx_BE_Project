from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from network_monitoring_tool.views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    
    path("admin/", admin.site.urls),

    # Auth
    path("api/auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Users app routes>>>
    path("api/users/", include("users.urls")),

    # Devices app routes>>>
    path("api/devices/", include("devices.urls")),

    # Audit app routes>>>
    path("api/audit/", include("audit.urls")),
    path("audit/", include("audit.urls")),

    #  Metrics
    path("metrics/", include("metrics.urls")),

    # alerts
    path("alerts/", include("alerts.urls")),
   
]
