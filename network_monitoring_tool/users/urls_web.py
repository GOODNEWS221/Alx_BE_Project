from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserListCreateView, UserDetailView, RoleListCreateView, RoleDetailView

urlpatterns = [
    # Auth
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Users (backend-only)
    path("", UserListCreateView.as_view(), name="user-list-create"),  # GET list / POST create
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),  # GET/PUT/DELETE

    # Roles
    path("roles/", RoleListCreateView.as_view(), name="role-list-create"),
    path("roles/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),
]
