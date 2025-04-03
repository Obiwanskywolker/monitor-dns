from flask import Flask
from markupsafe import Markup
import requests
import time
from flask import render_template_string

app = Flask(__name__)

servers = {
    "ZEUS": {
        "Ztcentral": "http://ztcentral.top:80",
        "AplusHM": "http://aplushm.top",
        "Strmg": "http://strmg.top",
        "Newxczs": "http://newxczs.top",
    },
    "CLUB": {
        "AFS4Zer": "http://afs4zer.vip:80",
    },
    "UNIPLAY": {
        "Ztuni": "http://ztuni.top:80",
        "Testezeiro": "http://testezeiro.com:80",
    },
    "POWERPLAY": {
        "Techon": "http://techon.one:80",
    },
    "P2CINE": {
        "Tuptu1": "https://tuptu1.live",
        "Tyuo22": "https://tyuo22.club",
        "AB22": "https://ab22.store",
    },
    "LIVE21": {
        "Tojole": "http://tojole.net:80",
    },
    "BXPLAY": {
        "BXPLux": "http://bxplux.top:80",
    },
    "ELITE": {
        "BandNews": "http://bandnews.asia:80",
    },
    "BLAZE": {
        "CDN Trek": "http://cdntrek.xyz:80",
        "Natkcz": "http://natkcz.xyz:80",
    }
}

status_data = {}

@app.route('/')
def monitor():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Monitor de DNS - Uptime</title>
        <style>
            body {
                font-family: Arial;
                background-color: #1e1e1e;
                color: white;
                text-align: center;
            }
            h1 { color: #00ff99; }
            table {
                margin: auto;
                border-collapse: collapse;
                width: 80%;
            }
            th, td {
                padding: 10px;
                border: 1px solid #444;
            }
            th {
                background-color: #333;
            }
            tr:nth-child(even) {
                background-color: #2c2c2c;
            }
        </style>
    </head>
    <body>
        <h1>🌐 Top 5 Servidores por Uptime</h1>
        <table>
            <tr><th>Servidor</th><th>Grupo</th><th>Uptime (horas)</th><th>Status</th></tr>
    """

    ranking = []
    for group, dns_list in servers.items():
        for name, url in dns_list.items():
            if name not in status_data:
                status_data[name] = {
                    "group": group,
                    "url": url,
                    "status": True,
                    "start_time": time.time()
                }

            try:
                response = requests.get(url, timeout=3)
                online = response.status_code == 200
            except:
                online = False

            if not online:
                status_data[name]["status"] = False
                status_data[name]["start_time"] = time.time()
            else:
                status_data[name]["status"] = True

            uptime = (time.time() - status_data[name]["start_time"]) / 3600
            ranking.append({
                "name": name,
                "group": group,
                "uptime": round(uptime, 2),
                "status": "🟢" if status_data[name]["status"] else "🔴"
            })

    top5 = sorted(ranking, key=lambda x: x['uptime'], reverse=True)[:5]

    for item in top5:
        html += f"<tr><td>{item['name']}</td><td>{item['group']}</td><td>{item['uptime']}</td><td>{item['status']}</td></tr>"

    html += """
        </table>
        <p style='margin-top:20px; color: gray;'>Atualizado automaticamente a cada 5 minutos.</p>
    </body>
    </html>
    """

    return render_template_string(Markup(html))