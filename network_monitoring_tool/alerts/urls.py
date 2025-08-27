from django.urls import path
from .views import AlertListCreateView, AlertDetailView, alert_list

urlpatterns = [
    # API
    path('api/alerts/', AlertListCreateView.as_view(), name='alert-list'),
    path('api/alerts/<int:pk>/', AlertDetailView.as_view(), name='alert-detail'),

    # Template
    path('alerts/', alert_list, name='alert-list-page'),
]