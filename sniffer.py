import scapy.all as scapy
import json

# Function to get protocol name
def get_protocol(protocol):
    if protocol == 6:
        return "TCP"
    elif protocol == 17:
        return "UDP"
    elif protocol == 1:
        return "ICMP"
    return "Unknown"

# Function to get service name from port
def get_service(port):
    mapping = {
        80: "HTTP",
        443: "HTTPS",
        53: "DNS",
        22: "SSH",
        1900: "SSDP",
       
        69: "TFTP",
        161: "SNMP",
    }
    return mapping.get(port, "Unknown")

# Function to process each packet
def process_packet(packet):
    if packet.haslayer(scapy.IP):
        # Extract packet information
        packet_info = {
            "time": packet.time,
            "src": packet[scapy.IP].src,
            "dst": packet[scapy.IP].dst,
            "protocol": get_protocol(packet.proto),
            "src_port": packet.sport if packet.haslayer(scapy.TCP) else 'N/A',
            "dst_port": packet.dport if packet.haslayer(scapy.TCP) else 'N/A',
            "size": len(packet),
            "service": get_service(packet.sport) if packet.haslayer(scapy.TCP) else "N/A"  # TCP service, N/A for others
        }
        print(packet_info)  # Log the packet info
        return packet_info
    return None

# Capture live packets using Scapy
def start_sniffing():
    scapy.sniff(filter="ip", prn=process_packet, store=False)  # Sniff IP packets