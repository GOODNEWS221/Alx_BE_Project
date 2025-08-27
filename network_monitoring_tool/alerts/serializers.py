from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)

    class Meta:
        model = Alert
        fields = [
            'id', 'device', 'device_name', 'metric_type',
            'threshold', 'value', 'status', 'timestamp',
            'resolved_at', 'description'
        ]