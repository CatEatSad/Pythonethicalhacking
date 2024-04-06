import netfilterqueue
import scapy.all as scapy
import re


# only work with http


def set_load(packet, load):
    packet[scapy.Raw].load = load
    # 301 move permanently redirect link to the location we set
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        scapy_packet.show()
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
