
from flask import Flask, render_template_string
import requests
import time

app = Flask(__name__)

DNS_LIST = [
    {"name": "Tuptu1", "url": "http://tuptu1.xyz"},
    {"name": "Techon", "url": "http://techon.one"},
    {"name": "Testezeiro", "url": "http://testezeiro.com"},
    {"name": "Ztuni", "url": "http://ztuni.top:80"},
    {"name": "Aplushm", "url": "http://aplushm.top"},
    {"name": "Newxczs", "url": "http://newxczs.top"},
    {"name": "Strmg", "url": "http://strmg.top"},
    {"name": "Ztcentral", "url": "http://ztcentral.top"}
]

last_check = {}

def check_status():
    for dns in DNS_LIST:
        name = dns["name"]
        url = dns["url"]
        try:
            start = time.time()
            response = requests.get(url, timeout=5)
            end = time.time()
            status = "Online" if response.status_code == 200 else f"Erro {response.status_code}"
            latency = round((end - start) * 1000)
        except Exception as e:
            status = "Offline"
            latency = "-"
        if name not in last_check:
            last_check[name] = {
                "status": status,
                "latency": latency,
                "last_online": time.time() if status == "Online" else None,
                "uptime_days": 0
            }
        else:
            if status == "Online":
                if last_check[name]["last_online"]:
                    elapsed = time.time() - last_check[name]["last_online"]
                    last_check[name]["uptime_days"] = round(elapsed / 86400, 2)
                else:
                    last_check[name]["last_online"] = time.time()
            last_check[name]["status"] = status
            last_check[name]["latency"] = latency

@app.route("/")
def index():
    check_status()
    return render_template_string("""
    <html>
        <head>
            <title>Status dos DNS</title>
            <meta http-equiv="refresh" content="300">
            <style>
                body { font-family: Arial; background-color: #f2f2f2; padding: 20px; }
                table { border-collapse: collapse; width: 100%; background: #fff; }
                th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
                th { background-color: #4CAF50; color: white; }
            </style>
        </head>
        <body>
            <h2>Status dos Servidores DNS</h2>
            <table>
                <tr>
                    <th>Nome da DNS</th>
                    <th>Endereço</th>
                    <th>Status</th>
                    <th>Latência (ms)</th>
                    <th>Uptime (dias)</th>
                </tr>
                {% for dns in dns_list %}
                <tr>
                    <td>{{ dns["name"] }}</td>
                    <td>{{ dns["url"] }}</td>
                    <td>{{ status[dns["name"]]["status"] }}</td>
                    <td>{{ status[dns["name"]]["latency"] }}</td>
                    <td>{{ status[dns["name"]]["uptime_days"] }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
    </html>
    """, dns_list=DNS_LIST, status=last_check)
