from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from devices.models import NetworkDevice
from metrics.models import DeviceMetric
from alerts.models import Alert
from audit.models import AuditLog

@login_required
def dashboard(request):
    # Device stats
    total_devices = NetworkDevice.objects.count()
    online_devices = NetworkDevice.objects.filter(status="online").count()
    offline_devices = NetworkDevice.objects.filter(status="offline").count()

    # Latest metrics (last 5)
    latest_metrics = DeviceMetric.objects.order_by("-timestamp")[:5]

    # Active alerts
    active_alerts = Alert.objects.filter(status="active").count()

    # Recent audit logs (last 5)
    recent_audits = AuditLog.objects.order_by("-timestamp")[:5]

    context = {
        "total_devices": total_devices,
        "online_devices": online_devices,
        "offline_devices": offline_devices,
        "latest_metrics": latest_metrics,
        "active_alerts": active_alerts,
        "recent_audits": recent_audits,
    }

    return render(request, "dashboard.html", context)
