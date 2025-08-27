from django import forms
from .models import DeviceMetric

class DeviceMetricForm(forms.ModelForm):
    class Meta:
        model = DeviceMetric
        fields = ["device", "metric_type", "value"]
        widgets = {
            "device": forms.Select(attrs={"class": "form-control"}),
            "metric_type": forms.Select(attrs={"class": "form-control"}),
            "value": forms.NumberInput(attrs={"class": "form-control"}),
        }

        