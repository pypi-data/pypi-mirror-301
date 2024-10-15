from ttlinks.ipservice.ip_configs import IPv4WildCardConfig
from ttlinks.protocol_stack.network_layer.ICMP.icmp_manager import ICMPPingManager

if __name__ == '__main__':
    manager = ICMPPingManager(semaphore=2000)
    ips = IPv4WildCardConfig('192.168.0.0 0.0.1.255').get_hosts()
    # ips = IPv4SubnetConfig('192.168.1.0/24').get_hosts()
    # ips = IPv4SubnetConfig('192.168.1.20/32').get_hosts()
    responses = manager.ping_multiple(ips, timeout=2, interval=1, count=2, verbose=True)
    print(responses)