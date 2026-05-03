document.getElementById("startBtn").addEventListener("click", startMonitoring);
document.getElementById("stopBtn").addEventListener("click", stopMonitoring);
document.getElementById("filterBtn").addEventListener("click", filterData);
document.getElementById("resetBtn").addEventListener("click", resetFilter); // ✅ reset button

let refreshInterval = null;

function startMonitoring() {
    fetch('/start_monitoring')
        .then(r => r.json())
        .then(data => {
            console.log("Started:", data);
            updateStatus("🟢 Monitoring active...");
            if (!refreshInterval) {
                refreshInterval = setInterval(() => {
                    fetchLatestPackets();
                    fetchStats();          // ✅ update stats every 2 seconds
                }, 2000);
            }
        })
        .catch(err => console.error("Start error:", err));
}

function stopMonitoring() {
    fetch('/stop_monitoring')
        .then(r => r.json())
        .then(data => {
            console.log("Stopped:", data);
            updateStatus("🔴 Monitoring stopped — showing captured packets");
            clearInterval(refreshInterval);
            refreshInterval = null;
            fetchLatestPackets();  // final fetch to keep packets visible
            fetchStats();          // ✅ final stats update
        })
        .catch(err => console.error("Stop error:", err));
}

function fetchLatestPackets() {
    let protocol = document.getElementById("protocolFilter").value;
    let sourceIp = document.getElementById("sourceIpFilter").value.trim();
    let destinationIp = document.getElementById("destinationIpFilter").value.trim();

    fetch(`/get_packets?protocol=${protocol}&sourceIp=${sourceIp}&destinationIp=${destinationIp}`)
        .then(r => r.json())
        .then(data => {
            console.log(`Received ${data.length} packets`);
            updateTable(data);
        })
        .catch(err => console.error("Fetch error:", err));
}

// ✅ fetch and display statistics
function fetchStats() {
    fetch('/get_stats')
        .then(r => r.json())
        .then(data => {
            document.getElementById("statTotal").innerText = data.total;
            document.getElementById("statTCP").innerText   = data.tcp;
            document.getElementById("statUDP").innerText   = data.udp;
            document.getElementById("statICMP").innerText  = data.icmp;
            document.getElementById("statAvg").innerText   = data.avg_size;
        })
        .catch(err => console.error("Stats error:", err));
}

function filterData() {
    fetchLatestPackets();
}

// ✅ reset all filters and reload all packets
function resetFilter() {
    document.getElementById("protocolFilter").value  = "All";
    document.getElementById("sourceIpFilter").value  = "";
    document.getElementById("destinationIpFilter").value = "";
    fetchLatestPackets();
}

function updateTable(data) {
    const tableBody = document.getElementById("dataBody");
    tableBody.innerHTML = "";

    if (data.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='8' style='text-align:center'>No data available</td></tr>"; // ✅ colspan 8
        return;
    }

    data.forEach(packet => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${new Date(packet.time * 1000).toLocaleTimeString()}</td>
            <td>${packet.src}</td>
            <td>${packet.dst}</td>
            <td>${packet.protocol}</td>
            <td>${packet.service}</td>           <!-- ✅ service column -->
            <td>${packet.size} bytes</td>
            <td>${packet.src_port}</td>
            <td>${packet.dst_port}</td>
        `;
        tableBody.appendChild(row);
    });
}

function updateStatus(msg) {
    let statusEl = document.getElementById("status");
    if (statusEl) statusEl.innerText = msg;
}