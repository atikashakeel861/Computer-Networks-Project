import scapy.all as scapy
from flask import Flask, jsonify, request, render_template
import threading

app = Flask(__name__)

captured_packets = []
sniffing_active = False

def get_protocol_name(proto_num):
    return {6: "TCP", 17: "UDP", 1: "ICMP"}.get(proto_num, "Unknown")

def get_service(port):
    if port == 'N/A':
        return 'N/A'
    mapping = {
        80: "HTTP", 443: "HTTPS", 53: "DNS", 22: "SSH",
        21: "FTP", 25: "SMTP", 110: "POP3", 143: "IMAP",
        3306: "MySQL", 3389: "RDP", 1900: "SSDP",
        67: "DHCP", 68: "DHCP", 123: "NTP"
    }
    return mapping.get(port, "Unknown")

def packet_sniffer():
    global sniffing_active

    def packet_callback(packet):
        if packet.haslayer(scapy.IP):

            if packet.haslayer(scapy.TCP):
                src_port = packet[scapy.TCP].sport
                dst_port = packet[scapy.TCP].dport
            elif packet.haslayer(scapy.UDP):
                src_port = packet[scapy.UDP].sport
                dst_port = packet[scapy.UDP].dport
            else:
                src_port = 'N/A'
                dst_port = 'N/A'

            packet_info = {
                'time': packet.time,
                'src': packet[scapy.IP].src,
                'dst': packet[scapy.IP].dst,
                'protocol': get_protocol_name(packet[scapy.IP].proto),
                'size': len(packet),
                'src_port': src_port,
                'dst_port': dst_port,
                'service': get_service(dst_port),
            }
            captured_packets.append(packet_info)
            print(f"Captured: {packet_info}")

    while sniffing_active:
        scapy.sniff(
            filter="tcp or udp or icmp",
            prn=packet_callback,
            store=0,
            timeout=1
        )

def start_sniffing():
    global sniffing_active
    sniffing_active = True
    t = threading.Thread(target=packet_sniffer)
    t.daemon = True
    t.start()

@app.route('/start_monitoring')
def start_monitoring():
    global captured_packets
    captured_packets = []
    start_sniffing()
    return jsonify({"status": "monitoring started"})

@app.route('/stop_monitoring')
def stop_monitoring():
    global sniffing_active
    sniffing_active = False
    return jsonify({"status": "monitoring stopped"})

@app.route('/get_packets')
def get_packets():
    protocol = request.args.get('protocol', 'All')
    source_ip = request.args.get('sourceIp', '')
    destination_ip = request.args.get('destinationIp', '')

    filtered = [
        p for p in captured_packets
        if (protocol == 'All' or p['protocol'] == protocol) and
           (not source_ip or p['src'] == source_ip) and
           (not destination_ip or p['dst'] == destination_ip)
    ]
    return jsonify(filtered)


@app.route('/get_stats')
def get_stats():
    total = len(captured_packets)
    tcp   = sum(1 for p in captured_packets if p['protocol'] == 'TCP')
    udp   = sum(1 for p in captured_packets if p['protocol'] == 'UDP')
    icmp  = sum(1 for p in captured_packets if p['protocol'] == 'ICMP')
    avg_size = round(sum(p['size'] for p in captured_packets) / total, 2) if total > 0 else 0
    return jsonify({"total": total, "tcp": tcp, "udp": udp, "icmp": icmp, "avg_size": avg_size})

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)