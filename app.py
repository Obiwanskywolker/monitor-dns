
from flask import Flask, render_template_string
import socket
from urllib.parse import urlparse
import threading
import time

app = Flask(__name__)

servers = [
    ("ZEUS", "Ztcentral", "http://ztcentral.top:80"),
    ("ZEUS", "AplusHM", "http://aplushm.top"),
    ("ZEUS", "Strmg", "http://strmg.top"),
    ("ZEUS", "Newxczs", "http://newxczs.top"),
    ("CLUB", "AFS4Zer", "http://afs4zer.vip:80"),
    ("UNIPLAY", "Ztuni", "http://ztuni.top:80"),
    ("UNIPLAY", "Testezeiro", "http://testezeiro.com:80"),
    ("POWERPLAY", "Techon", "http://techon.one:80"),
    ("P2CINE", "Tuptu1", "https://tuptu1.live"),
    ("P2CINE", "Tyuo22", "https://tyuo22.club"),
    ("P2CINE", "AB22", "https://ab22.store"),
    ("LIVE21", "Tojole", "http://tojole.net:80"),
    ("BXPLAY", "BXPLux", "http://bxplux.top:80"),
    ("ELITE", "BandNews", "http://bandnews.asia:80"),
    ("BLAZE", "CDN Trek", "http://cdntrek.xyz:80"),
    ("BLAZE", "Natkcz", "http://natkcz.xyz:80"),
]

status_data = {}

def check_server(name, url):
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        with socket.create_connection((host, port), timeout=5):
            return "🟢 Online"
    except Exception:
        return "🔴 Offline"

def update_status():
    while True:
        for group, name, url in servers:
            status = check_server(name, url)
            status_data[name] = {
                "group": group,
                "url": url,
                "status": status,
                "uptime": 100 if status == "🟢 Online" else 0
            }
        time.sleep(300)

threading.Thread(target=update_status, daemon=True).start()

@app.route("/")
def index():
    rows = ""
    for name, data in status_data.items():
        rows += f"<tr><td>{name}</td><td>{data['group']}</td><td>{data['uptime']}%</td><td>{data['status']}</td></tr>"
    html = f'''
    <html>
    <head>
        <meta charset="utf-8">
        <title>Monitor de DNS</title>
    </head>
    <body>
        <h2>🔎 Todos os Servidores</h2>
        <table border="1" cellpadding="10">
            <tr><th>Servidor</th><th>Grupo</th><th>Uptime</th><th>Status</th></tr>
            {rows}
        </table>
        <p>Atualizado a cada 5 minutos</p>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
