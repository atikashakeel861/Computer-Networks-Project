# Network Traffic Monitoring and Analysis Platform

**Student:** Atika Shakeel  
**Roll No:** BCSF24A035  
**Course:** Computer Networks  

---

## Project Description
A real-time network traffic monitoring system built with Python and Flask.
Captures live packets using Scapy and displays them in a web dashboard
with filtering and statistics.

---

## Features
- Real-time packet sniffing (TCP, UDP, ICMP)
- Web-based dashboard with auto-refresh every 2 seconds
- Displays: Time, Source IP, Destination IP, Protocol, Service, Size, Ports
- Filter by Protocol, Source IP, Destination IP
- Reset filter button
- Live statistics: Total packets, TCP/UDP/ICMP counts, Average size
- Packets persist after stopping monitoring

---

## Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3 | Backend logic |
| Flask | Web framework and API routes |
| Scapy | Live packet sniffing |
| HTML/CSS/JavaScript | Frontend interface |

---

---

## How to Run

### Requirements
- Python 3
- Windows (run as Administrator for packet sniffing)

### Install Dependencies
```bash
pip install flask scapy
```

### Run the App
```bash
python app.py
```

### Open in Browser
http://127.0.0.1:5000

### To Generate ICMP Packets
Open a separate Command Prompt and run:
```bash
ping 8.8.8.8
```

---

## Dataset
This project uses **real-time packet sniffing** instead of a static dataset.
Scapy captures live IP packets directly from the network interface.
No CSV file is required.

---
