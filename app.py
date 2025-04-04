from flask import Flask, render_template
import http.client
from datetime import datetime, timedelta
import threading
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

PORTAS = [80, 8080]
status_cache = {}
lock = threading.Lock()

def check_http_status(host):
    for port in PORTAS:
        try:
            conn = http.client.HTTPConnection(host, port=port, timeout=4)
            conn.request("HEAD", "/")
            response = conn.getresponse()
            # Considera online se qualquer resposta for recebida
            return True
        except Exception:
            continue
    return False

def update_statuses():
    while True:
        with lock:
            now = datetime.utcnow()
            for s in servers:
                name = s["name"]
                was_online = status_cache.get(name, {}).get("status", False)
                uptime_start = status_cache.get(name, {}).get("uptime_start")

                is_online = check_http_status(s["url"])

                if is_online:
                    if not was_online:
                        uptime_start = now
                    elapsed = (now - uptime_start).total_seconds() / 3600 if uptime_start else 0
                else:
                    uptime_start = None
                    elapsed = 0

                status_cache[name] = {
                    "status": is_online,
                    "uptime_start": uptime_start,
                    "uptime_hours": round(elapsed, 2)
                }

        time.sleep(300)  # Atualiza a cada 5 minutos

@app.route('/')
def home():
    with lock:
        result = []
        for s in servers:
            cache = status_cache.get(s["name"], {})
            result.append({
                "name": s["name"],
                "group": s["group"],
                "status": cache.get("status", False),
                "uptime_hours": cache.get("uptime_hours", 0.0)
            })
    return render_template("status.html", servidores=result)

if __name__ == '__main__':
    t = threading.Thread(target=update_statuses, daemon=True)
    t.start()
    app.run(debug=True, port=5000)
