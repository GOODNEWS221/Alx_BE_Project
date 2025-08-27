from rest_framework import serializers
from metrics.models import NetworkDevice, DeviceMetric

class NetworkDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDevice
        fields = "__all__"


class DeviceMetricSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source="device.name", read_only=True)

    class Meta:
        model = DeviceMetric
        fields = ["id", "device", "device_name", "metric_type", "value", "timestamp"]
