from pysnmp.hlapi import *
from ping3 import ping
from datetime import datetime
from django.utils.timezone import make_aware
from metrics.models import NetworkDevice, DeviceMetric   # fixed: metric (singular), NetworkDevice

def ping_device(device: NetworkDevice):
    """
    Ping a device and log latency in ms.
    """
    response_time = ping(device.ip_address, timeout=2)
    timestamp = make_aware(datetime.now())

    metric = DeviceMetric.objects.create(
        device=device,
        metric_type="ping",
        value=response_time * 1000 if response_time else None,  # convert to ms
        timestamp=timestamp
    )

    return metric


def snmp_get(ip, community, oid, port=161):   # fixed: oid spelling + added colon
    """
    Perform SNMP GET request.
    """
    iterator = getCmd( # type: ignore
        SnmpEngine(), # type: ignore
        CommunityData(community, mpModel=0),  # SNMP v2c # type: ignore
        UdpTransportTarget((ip, port)), # type: ignore
        ContextData(), # type: ignore
        ObjectType(ObjectIdentity(oid)) # type: ignore
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        return None
    elif errorStatus:
        return None
    else:
        for varBind in varBinds:
            return str(varBind[1])