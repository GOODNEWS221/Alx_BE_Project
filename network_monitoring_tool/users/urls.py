from django.urls import path
from .views import (
    RegisterUserView,
    UserListView,
    UserDetailView,
    RoleListCreateView,
    RoleDetailView,
)

urlpatterns = [
    # User endpoints
    path("register/", RegisterUserView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),

    # Role endpoints
    path("roles/", RoleListCreateView.as_view(), name="role-list-create"),
    path("roles/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),
]

