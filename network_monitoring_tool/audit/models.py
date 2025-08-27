from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    ACTIONS = (
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("other", "Other"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs"
    )
    action = models.CharField(max_length=20, choices=ACTIONS)
    model_name = models.CharField(max_length=100)   # e.g. "NetworkDevice"
    object_id = models.CharField(max_length=100, blank=True, null=True)  # record ID
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.user} - {self.action} {self.model_name} ({self.object_id})"

# Create your models here.
