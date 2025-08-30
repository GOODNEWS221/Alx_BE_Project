from django.urls import path
from .views import AlertListCreateView, AlertDetailView, alert_list

urlpatterns = [
    # API
    path('', AlertListCreateView.as_view(), name='alert-list'),
    
    # Template
]