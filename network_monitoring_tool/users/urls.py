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

from django.urls import path
from . import views

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

    #templates
    path("", views.user_list, name="user-list"),
    path("add/", views.user_add, name="user-add"),
    path("<int:pk>/edit/", views.user_edit, name="user-edit"),
    path("<int:pk>/delete/", views.user_delete, name="user-delete"),

    # Roles
    path("roles/", views.role_list, name="role-list"),
    path("roles/add/", views.role_add, name="role-add"),
    path("roles/<int:pk>/edit/", views.role_edit, name="role-edit"),
    path("roles/<int:pk>/delete/", views.role_delete, name="role-delete"),
]
