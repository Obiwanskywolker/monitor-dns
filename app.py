from flask import Flask, render_template
import requests
from datetime import datetime
from urllib.parse import urlparse
import time

app = Flask(__name__)

# Lista de servidores IPTV
servers = [
    {"name": "Ztcentral", "url": "ztcentral.top", "group": "ZEUS"},
    {"name": "AplusHM", "url": "aplushm.top", "group": "ZEUS"},
    {"name": "Strmg", "url": "strmg.top", "group": "ZEUS"},
    {"name": "Newxczs", "url": "newxczs.top", "group": "ZEUS"},
    {"name": "AFS4Zer", "url": "afs4zer.vip", "group": "CLUB"},
    {"name": "Ztuni", "url": "ztuni.top", "group": "UNIPLAY"},
    {"name": "Testezeiro", "url": "testezeiro.com", "group": "UNIPLAY"},
    {"name": "Techon", "url": "techon.one", "group": "POWERPLAY"},
    {"name": "Tuptu1", "url": "tuptu1.live", "group": "P2CINE"},
    {"name": "Tyuo22", "url": "tyuo22.club", "group": "P2CINE"},
    {"name": "AB22", "url": "ab22.store", "group": "P2CINE"},
    {"name": "Tojole", "url": "tojole.net", "group": "LIVE21"},
    {"name": "BXPLux", "url": "bxplux.top", "group": "BXPLAY"},
    {"name": "BandNews", "url": "bandnews.asia", "group": "ELITE"},
    {"name": "CDN Trek", "url": "cdntrek.xyz", "group": "BLAZE"},
    {"name": "Natkcz", "url": "natkcz.xyz", "group": "BLAZE"},
]

# Portas comuns usadas por servidores IPTV
PORTAS = [80, 81, 443, 8080]


def check_status(server):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    for port in PORTAS:
        try:
            protocol = "https" if port == 443 else "http"
            url = f"{protocol}://{server['url']}:{port}"
            response = requests.get(url, headers=headers, timeout=2)
            if response.status_code == 200:
                return True
        except:
            continue
    return False


@app.route('/')
def home():
    result = []
    for s in servers:
        status = check_status(s)
        result.append({
            "name": s["name"],
            "group": s["group"],
            "status": status
        })
        time.sleep(0.2)  # Reduz o uso de memória e evita sobrecarga
    return render_template("status.html", servidores=result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
