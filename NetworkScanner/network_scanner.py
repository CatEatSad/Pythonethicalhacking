import scapy.all as scapy


# https://scapy.readthedocs.io/en/latest/ scapy's documentation

def scan(ip):
    # scapy.arping(ip)  # Scan ip
    arp_request = scapy.ARP(pdst=ip)  # select the object ( created and select)
    # arp_request.show()
    # print(arp_request.summary())  # summary =  a summary of the current object that we just created
    # scapy.ls(scapy.ARP())

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # broadcast.show()
    # scapy.ls(scapy.Ether())
    # print(broadcast.summary())

    arp_request_broadcast = broadcast / arp_request # combine frames to broadcast address , must be same type to combine
    # print(type(arp_request))
    # print(type(broadcast))
    # print(type(arp_request_broadcast))
    # print(arp_request_broadcast.summary())
    # arp_request_broadcast.show()
    scapy.srp(arp_request_broadcast)  # function for sending packet
    # and return 2 value : first is anwered , second is unanswered
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # timeout : if it doesn't get response wait 1 second and move on
    # verbose : default is true , if it true it tell you that it will show all things it has to u
    # print(answered_list.summary())

    client_list = []
    for elements in answered_list:
        client_dict = {"ip": elements[1].psrc, "mac": elements[1].hwsrc}
        client_list.append(client_dict)
        #print(elements[1].psrc + "\t\t" + elements[1].hwsrc)
    return client_list


def print_rs(rs_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------------")
    for client in rs_list:
        print(client)


# element in arp list : first element is the request sent
# the second is the answer


scan_rs = scan("192.168.88.0/24")
print_rs(scan_rs)
