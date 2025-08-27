from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_list, name="user-list"),  # List of users (web view)
    path("add/", views.user_add, name="user-add"),
    path("<int:pk>/edit/", views.user_edit, name="user-edit"),
    path("<int:pk>/delete/", views.user_delete, name="user-delete"),
]