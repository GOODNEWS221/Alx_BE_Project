from pysnmp.hlapi import *
from ping3 import ping
from datetime import datetime
from django.utils.timezone import make_aware
from metrics.models import NetworkDevice, DeviceMetric


def ping_device(device: NetworkDevice):
    """
    Ping a device and log latency in ms.
    """
    response_time = ping(device.ip_address, timeout=2)
    timestamp = make_aware(datetime.now())

    metric = DeviceMetric.objects.create(
        device=device,
        metric_type="ping",
        value=response_time * 1000 if response_time else None,  # ms or None if failed
        timestamp=timestamp
    )

    return metric


def snmp_get(ip, community, oid, port=161):
    """
    Perform SNMP GET request.
    """
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),  # SNMP v2c
        UdpTransportTarget((ip, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication or errorStatus:
        return None

    for varBind in varBinds:
        return str(varBind[1])


def log_snmp_metric(device: NetworkDevice, oid: str, metric_type: str):
    """
    Fetch SNMP data from a device and log it in DeviceMetric.
    """
    value = snmp_get(device.ip_address, device.snmp_community, oid)
    timestamp = make_aware(datetime.now())

    metric = DeviceMetric.objects.create(
        device=device,
        metric_type=metric_type,
        value=value,
        timestamp=timestamp
    )

    return metric
