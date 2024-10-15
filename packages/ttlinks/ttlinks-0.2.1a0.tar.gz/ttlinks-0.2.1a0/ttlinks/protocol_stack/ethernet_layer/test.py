from ttlinks.protocol_stack.ethernet_layer.test_packets import TestUnits
from ttlinks.protocol_stack.ethernet_layer.ethernet_units import EthernetUnitFactory


if __name__ == '__main__':
    test_unit = TestUnits()

    frame_factory = EthernetUnitFactory
    ethernet_frame = frame_factory.create_unit(test_unit.icmp_ttl_exceeded)
    print('ethernet_frame', ethernet_frame.summary)
    packet_header = ethernet_frame.payload
    print('packet_header', packet_header.summary)
    packet_payload = packet_header.payload
    print('packet_payload', packet_payload.summary)
    print('icmp_payload', packet_payload.payload)
    print('icmp_payload', packet_payload.payload.summary)
    print('icmp_payload2', packet_payload.payload.payload)
