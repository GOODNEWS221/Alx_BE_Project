from django.db import models
from metrics.models import NetworkDevice

class Alert(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('resolved', 'Resolved'),
    )

    device = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE, related_name='alerts')
    metric_type = models.CharField(max_length=50)  # e.g., "cpu", "memory"
    threshold = models.FloatField()  # threshold value
    value = models.FloatField()  # actual value when alert triggered
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.device.name} - {self.metric_type} alert ({self.status})"

# Create your models here.
