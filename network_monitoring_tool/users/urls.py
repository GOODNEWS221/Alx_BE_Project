# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterUserView, 
    UserListView, UserDetailView, 
    RoleListCreateView, RoleDetailView
)

urlpatterns = [
    # Auth
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Users
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),

    # Roles
    path("roles/", RoleListCreateView.as_view(), name="role-list"),
    path("roles/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),
]
