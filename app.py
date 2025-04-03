import requests
import time
import json
from flask import Flask, render_template_string
from threading import Thread
import os

app = Flask(__name__)

SERVIDORES = {
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

DATA_FILE = "data.json"

def verificar_servidores():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}

    while True:
        for grupo, servidores in SERVIDORES.items():
            for nome, url in servidores.items():
                if nome not in data:
                    data[nome] = {"uptime_horas": 0, "status": False, "group": grupo}
                try:
                    response = requests.get(url, timeout=5, verify=False)
                    if response.status_code == 200:
                        data[nome]["uptime_horas"] += round(5 / 3600, 4)
                        data[nome]["status"] = True
                    else:
                        data[nome]["status"] = False
                except:
                    data[nome]["status"] = False

        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

        time.sleep(300)

@app.route("/")
def index():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}

    ranking = [
        {"nome": nome, "group": info["group"], "uptime_horas": round(info["uptime_horas"], 2), "status": info["status"]}
        for nome, info in data.items()
    ]

    top5 = sorted(ranking, key=lambda x: x["uptime_horas"], reverse=True)[:5]

    html = """
    <html>
    <head>
        <title>Monitor de DNS - Uptime</title>
        <style>
            body {
                font-family: Arial;
                background-color: #1e1e1e;
                color: white;
                margin: 0;
                padding: 0;
            }
            h2 {
                text-align: center;
                color: lime;
                padding-top: 20px;
            }
            .top5 {
                position: fixed;
                top: 10px;
                left: 10px;
                background-color: #111;
                padding: 10px;
                border: 1px solid lime;
                border-radius: 8px;
            }
            .top5 h3 {
                margin-top: 0;
                color: lime;
            }
            table {
                width: 90%;
                margin: 80px auto 20px auto;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #444;
                padding: 10px;
                text-align: center;
            }
            th {
                background-color: #333;
            }
            .status-ok {
                color: lime;
            }
            .status-fail {
                color: red;
            }
            .footer {
                text-align: center;
                font-size: 12px;
                color: #aaa;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="top5">
            <h3>🌐 Top 5 Uptime</h3>
            <ul>
                """ + "".join([f"<li>{srv['nome']}</li>" for srv in top5]) + """
            </ul>
        </div>
        <h2>📊 Todos os Servidores</h2>
        <table>
            <tr>
                <th>Servidor</th>
                <th>Grupo</th>
                <th>Uptime (horas)</th>
                <th>Status</th>
            </tr>
    """

    for srv in ranking:
        html += f"""
        <tr>
            <td>{srv['nome']}</td>
            <td>{srv['group']}</td>
            <td>{srv['uptime_horas']}</td>
            <td class="{ 'status-ok' if srv['status'] else 'status-fail' }">
                {"🟢" if srv['status'] else "🔴"}
            </td>
        </tr>
        """

    html += """
        </table>
        <div class="footer">
            Atualizado automaticamente a cada 5 minutos.
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    Thread(target=verificar_servidores, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))