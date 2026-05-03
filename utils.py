# utils.py
def get_service(port):
    mapping = {
        80: "HTTP",
        443: "HTTPS",
        53: "DNS",
        22: "SSH",
        1900: "SSDP"
    }
    return mapping.get(port, "Unknown")