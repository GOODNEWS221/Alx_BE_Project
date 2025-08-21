from rest_framework import serializers
from .models import DeviceGroup, NetworkDevice

class DeviceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceGroup
        fields = ["id", "name", "description"]


class NetworkDeviceSerializer(serializers.ModelSerializer):
    group = DeviceGroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceGroup.objects.all(), source="group", write_only=True, required=False
    )

    class Meta:
        model = NetworkDevice
        fields = [
            "id", "name", "ip_address", "device_type", "status",
            "location", "added_by", "group", "group_id", "added_at"
        ]
        read_only_fields = ["added_by", "added_at"]

    