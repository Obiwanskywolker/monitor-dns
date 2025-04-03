import requests
import time
import socket
from urllib.parse import urlparse
from flask import Flask, jsonify, render_template_string
import threading

app = Flask(__name__)

servers = {
    "ZEUS": [
        {"name": "Ztcentral", "url": "http://ztcentral.top:80"},
        {"name": "AplusHM", "url": "http://aplushm.top"},
        {"name": "Strmg", "url": "http://strmg.top"},
        {"name": "Newxczs", "url": "http://newxczs.top"},
    ],
    "CLUB": [{"name": "AFS4Zer", "url": "http://afs4zer.vip:80"}],
    "UNIPLAY": [
        {"name": "Ztuni", "url": "http://ztuni.top:80"},
        {"name": "Testezeiro", "url": "http://testezeiro.com:80"},
    ],
    "POWERPLAY": [{"name": "Techon", "url": "http://techon.one:80"}],
    "P2CINE": [
        {"name": "Tuptu1", "url": "https://tuptu1.live"},
        {"name": "Tyuo22", "url": "https://tyuo22.club"},
        {"name": "AB22", "url": "https://ab22.store"},
    ],
    "LIVE21": [{"name": "Tojole", "url": "http://tojole.net:80"}],
    "BXPLAY": [{"name": "BXPLux", "url": "http://bxplux.top:80"}],
    "ELITE": [{"name": "BandNews", "url": "http://bandnews.asia:80"}],
    "BLAZE": [
        {"name": "CDN Trek", "url": "http://cdntrek.xyz:80"},
        {"name": "Natkcz", "url": "http://natkcz.xyz:80"},
    ],
}

status_data = {
    group: {
        dns["name"]: {
            "url": dns["url"],
            "status": "Desconhecido",
            "uptime": 100.0,
            "failures": 0,
            "last_check": "-",
            "uptime_seconds": 0
        } for dns in dns_list
    } for group, dns_list in servers.items()
}

def check_dns():
    while True:
        for group, dns_list in servers.items():
            for dns in dns_list:
                name = dns["name"]
                url = dns["url"]
                try:
                    parsed = urlparse(url)
                    host = parsed.hostname
                    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
                    with socket.create_connection((host, port), timeout=5):
                        status_data[group][name]["status"] = "🟢 Online"
                        status_data[group][name]["uptime_seconds"] += 300
                except:
                    status_data[group][name]["status"] = "🔴 Offline"
                    status_data[group][name]["failures"] += 1

                status_data[group][name]["last_check"] = time.strftime("%d/%m %H:%M:%S")
                total_checks = (status_data[group][name]["uptime_seconds"] // 300) + status_data[group][name]["failures"]
                if total_checks > 0:
                    status_data[group][name]["uptime"] = round((status_data[group][name]["uptime_seconds"] / (total_checks * 300)) * 100, 2)
        time.sleep(300)

@app.route("/")
def index():
    top = []
    for group, dns_dict in status_data.items():
        for name, info in dns_dict.items():
            top.append({
                "group": group,
                "name": name,
                "uptime": info["uptime"],
                "status": info["status"],
                "horas": round(info["uptime_seconds"] / 3600, 1)
            })
    top5 = sorted(top, key=lambda x: x["uptime"], reverse=True)[:5]

    html = open("index.html").read()
    return render_template_string(html, top5=top5)

@app.route("/api/status")
def get_status():
    return jsonify(status_data)

if __name__ == "__main__":
    t = threading.Thread(target=check_dns, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)
