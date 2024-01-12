# !/usr/bin/env python Use the optparse library I showed you in the previous section to extend this program and make
# it take the IP range through a command line argument, let the argument be -t or --target, so users can call the
# program from terminal like so python network_scanner.py --t 10.0.2.1/24
#
# OR
#
# python network_scanner.py --target 10.0.2.1/24


import scapy.all as scapy
import argparse  # same optparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    options = parser.parse_args()
    print(options)
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n-------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)

# python exam.py --target 192.168.88.0/24
