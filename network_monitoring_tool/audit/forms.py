from django import forms
from .models import AuditLog

class AuditLogForm(forms.ModelForm):
    class Meta:
        model = AuditLog
        fields = ["user", "device", "action", "description"]