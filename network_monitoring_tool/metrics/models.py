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

    # 🔹 SNMP support
    snmp_community = models.CharField(max_length=100, default="public")
    snmp_port = models.PositiveIntegerField(default=161)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    group = models.ForeignKey(
        DeviceGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="devices"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class DeviceMetric(models.Model):
    METRIC_TYPES = (
        ("ping", "Ping"),
        ("cpu", "CPU"),
        ("memory", "Memory"),
        ("interface", "Interface"),
        ("custom", "Custom"),
    )

    device = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE, related_name="metrics")
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    value = models.FloatField(null=True, blank=True)  # e.g., latency ms, CPU %, memory %
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.device.name} - {self.metric_type} @ {self.timestamp}"


