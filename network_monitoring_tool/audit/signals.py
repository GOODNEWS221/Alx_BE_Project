from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.contrib.auth import get_user_model
from .models import AuditLog
from .middleware import get_current_user

User = get_user_model()


def create_audit_log(action, instance, details=""):
    AuditLog.objects.create(
        user=get_current_user(),
        action=action,
        model_name=instance.__class__.__name__,
        object_id=str(instance.pk),
        details=details,
    )

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    # Avoid logging the AuditLog model itself (to prevent infinite recursion)
    if sender == AuditLog:
        return

    if created:
        create_audit_log("create", instance, "Object created")
    else:
        create_audit_log("update", instance, "Object updated")


@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    if sender == AuditLog:
        return
    create_audit_log("delete", instance, "Object deleted")