from rest_framework import serializers
from .models import DeviceGroup, NetworkDevice


class DeviceGroupSerializer(serializers.ModelSerializer):
    """Serializer for grouping network devices."""
    
    class Meta:
        model = DeviceGroup
        fields = ["id", "name", "description"]


class NetworkDeviceSerializer(serializers.ModelSerializer):
    """Serializer for network devices with support for nested group representation."""
    
    # Show group details when reading
    group = DeviceGroupSerializer(read_only=True)

    # Allow assigning group by ID when creating/updating
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceGroup.objects.all(),
        source="group",  # map group_id -> group
        write_only=True,
        required=False
    )

    class Meta:
        model = NetworkDevice
        fields = [
            "id",
            "name",
            "ip_address",
            "device_type",
            "status",
            "location",
            "added_by",
            "group",       # nested output
            "group_id",    # input for group assignment
            "added_at",
        ]
        read_only_fields = ["added_by", "added_at"]
