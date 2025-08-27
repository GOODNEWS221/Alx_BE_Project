from django.core.management.base import BaseCommand
from metrics.models import NetworkDevice
from metrics.utils import ping_device, snmp_get
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Collect metrics from all devices"

    def handle(self, *args, **kwargs):
        devices = NetworkDevice.objects.all()
        for device in devices:
            self.stdout.write(f"Collecting metrics for {device.name} ({device.ip_address})")

            # Ping test
            ping_metric = ping_device(device)
            self.stdout.write(f"  Ping: {ping_metric.value} ms")

            # SNMP example (CPU usage OID — Cisco default example)
            if hasattr(device, "community"):  # ensure field exists in model
                cpu_usage = snmp_get(device.ip_address, device.community, ".1.3.6.1.4.1.9.2.1.57.0")
                if cpu_usage:
                    device.devicemetric_set.create(
                        metric_type="cpu",
                        value=cpu_usage,
                        timestamp=now()
                    )
                    self.stdout.write(f"  CPU: {cpu_usage}%")