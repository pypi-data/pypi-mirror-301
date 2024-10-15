from ttlinks.ipservice.ip_address import IPv4Addr, IPv6Addr
from ttlinks.ipservice.ip_converters import DecimalIPv4ConverterHandler, DecimalIPv6ConverterHandler
import ipaddress

from ttlinks.ipservice.ip_factory import IPv4Factory, IPv4TypeAddrBlocks
from ttlinks.macservice import MACType
from ttlinks.macservice.mac_factory import MACFactory

if __name__ == '__main__':
    mac_factory = MACFactory()
    macs= mac_factory.random_macs_batch(MACType.UNICAST, num_macs=5000)
    for mac in macs:
        if mac.oui:
            print(f'{mac} - {mac.oui.record['oui_type']} - {mac.oui.record['organization']}')

