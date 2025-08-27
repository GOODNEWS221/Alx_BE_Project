from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import AuditLog
from devices.models import NetworkDevice  # adjust if you want to monitor more models

User = get_user_model()

def create_audit_log(user, action, instance, details=""):
    """Helper function to create audit logs"""
    AuditLog.objects.create(
        user=user if isinstance(user, User) else None,
        action=action,
        model_name=instance.__class__.__name__,
        object_id=str(instance.pk),
        details=details
    )

# --- Track NetworkDevice creation and updates ---
@receiver(post_save, sender=NetworkDevice)
def log_device_save(sender, instance, created, **kwargs):
    if created:
        create_audit_log(user=None, action="create", instance=instance, details="Device created")
    else:
        create_audit_log(user=None, action="update", instance=instance, details="Device updated")

# --- Track NetworkDevice deletion ---
@receiver(post_delete, sender=NetworkDevice)
def log_device_delete(sender, instance, **kwargs):
    create_audit_log(user=None, action="delete", instance=instance, details="Device deleted")