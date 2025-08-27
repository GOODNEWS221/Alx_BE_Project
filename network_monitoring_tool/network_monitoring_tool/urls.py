from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
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
]
