from django.db import models
from django.conf import settings

class DeviceGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class NetworkDevice(models.Model):
    DEVICE_TYPES = (
        ("Router", "Router"),
        ("Switch", "Switch"),
        ("Firewall", "Firewall"),
        ("Server", "Server"),
        ("Other", "Other"),
    )

    STATUS_CHOICES = (
        ("online", "Online"),
        ("offline", "Offline"),
        ("unknown", "Unknown"),
    )

    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(unique=True)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unknown")
    location = models.CharField(max_length=100, blank=True, null=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    group = models.ForeignKey(
        DeviceGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="devices"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"