from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from network_monitoring_tool.views import dashboard
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Dashboard and authentication
    path("", dashboard, name="dashboard"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),  # logout via POST in base.html

    # Admin
    path("admin/", admin.site.urls),

    # JWT API login (POST only)
    path("api/auth/login/", TokenObtainPairView.as_view(), name="api-login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # App routes
    path("api/users/", include("users.urls")),
    path("api/devices/", include("devices.urls")),
    path("api/audit/", include("audit.urls")),
    path("audit/", include("audit.urls")),
    path("metrics/", include("metrics.urls")),
    path("alerts/", include("alerts.urls")),


        # Web URLs (HTML pages)
    path("users/", include("users.urls_web")),
    path("devices/", include("devices.urls_web")),
    path("metrics/", include("metrics.urls_web")),
    path("alerts/", include("alerts.urls_web")),
    path("audit/", include("audit.urls_web")),
]
