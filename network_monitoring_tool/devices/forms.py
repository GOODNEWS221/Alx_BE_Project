from django import forms
from .models import DeviceGroup, NetworkDevice

# --- Device Groups ---
class DeviceGroupForm(forms.ModelForm):
    class Meta:
        model = DeviceGroup
        fields = ["name", "description"]

# --- Network Devices ---
class NetworkDeviceForm(forms.ModelForm):
    class Meta:
        model = NetworkDevice
        fields = [
            "name", "ip_address", "device_type", "status",
            "location", "group"
        ]

        