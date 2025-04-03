
from flask import Flask, render_template_string
import requests
import json
import os
import threading
import time

app = Flask(__name__)

DATA_FILE = "data.json"
CHECK_INTERVAL = 300  # 5 minutos

# Lista de servidores
servers = {
    "ZEUS": {
        "Ztcentral": "http://ztcentral.top:80",
        "AplusHM": "http://aplushm.top",
        "Strmg": "http://strmg.top",
        "Newxczs": "http://newxczs.top"
    },
    "CLUB": {
        "AFS4Zer": "http://afs4zer.vip:80"
    },
    "UNIPLAY": {
        "Ztuni": "http://ztuni.top:80",
        "Testezeiro": "http://testezeiro.com:80"
    },
    "POWERPLAY": {
        "Techon": "http://techon.one:80"
    },
    "P2CINE": {
        "Tuptu1": "https://tuptu1.live",
        "Tyuo22": "https://tyuo22.club",
        "AB22": "https://ab22.store"
    },
    "LIVE21": {
        "Tojole": "http://tojole.net:80"
    },
    "BXPLAY": {
        "BXPLux": "http://bxplux.top:80"
    },
    "ELITE": {
        "BandNews": "http://bandnews.asia:80"
    },
    "BLAZE": {
        "CDN Trek": "http://cdntrek.xyz:80",
        "Natkcz": "http://natkcz.xyz:80"
    }
}

# Inicializa os dados
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def check_servers():
    data = load_data()
    while True:
        for group, srvrs in servers.items():
            for name, url in srvrs.items():
                try:
                    response = requests.get(url, timeout=5)
                    online = response.status_code == 200
                except:
                    online = False
                if name not in data:
                    data[name] = {
                        "uptime_horas": 0,
                        "status": online,
                        "group": group
                    }
                if online:
                    data[name]["uptime_horas"] += CHECK_INTERVAL / 3600
                    data[name]["status"] = True
                else:
                    data[name]["status"] = False
        save_data(data)
        time.sleep(CHECK_INTERVAL)

@app.route("/")
def index():
    data = load_data()
    ranking = [
        {
            "name": name,
            "group": info["group"],
            "uptime_horas": round(info["uptime_horas"], 2),
            "status": info["status"]
        }
        for name, info in data.items()
    ]
    top5 = sorted(ranking, key=lambda x: x["uptime_horas"], reverse=True)[:5]
    html = '''
    <html>
    <head>
        <title>Monitor de DNS - Uptime</title>
        <style>
            body { font-family: Arial; background-color: #111; color: white; }
            table { width: 90%; margin: auto; border-collapse: collapse; }
            th, td { padding: 10px; text-align: center; border-bottom: 1px solid #444; }
            th { background-color: #222; }
            .status-on { color: lime; }
            .status-off { color: red; }
            .top5-box {
                position: absolute;
                top: 10px;
                left: 10px;
                padding: 10px;
                border: 2px solid limegreen;
                border-radius: 10px;
                background-color: #000;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="top5-box">
            🌐 Top 5 Uptime<br>
            ''' + "<br>".join([s["name"] for s in top5]) + '''
        </div>
        <h2 style="text-align:center; color:lime;">📊 Todos os Servidores</h2>
        <table>
            <tr><th>Servidor</th><th>Grupo</th><th>Uptime (horas)</th><th>Status</th></tr>
    '''
    for s in ranking:
        status_icon = "🟢" if s["status"] else "🔴"
        html += f"<tr><td>{s['name']}</td><td>{s['group']}</td><td>{s['uptime_horas']}</td><td>{status_icon}</td></tr>"
    html += '''
        </table>
        <p style="text-align:center; color:gray;">Atualizado automaticamente a cada 5 minutos.</p>
    </body></html>
    '''
    return render_template_string(html)

if __name__ == "__main__":
    t = threading.Thread(target=check_servers)
    t.daemon = True
    t.start()
    app.run(host="0.0.0.0", port=10000)
