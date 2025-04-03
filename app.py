import time
import requests
from flask import Flask, Markup

app = Flask(__name__)
start_times = {}

SERVERS = {
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

def check_status(name, url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            if name not in start_times:
                start_times[name] = time.time()
            uptime = round((time.time() - start_times[name]) / 3600, 2)
            return uptime, "✅"
        else:
            start_times.pop(name, None)
            return 0, "❌"
    except:
        start_times.pop(name, None)
        return 0, "❌"

@app.route("/")
def home():
    ranking = []
    for group, servers in SERVERS.items():
        for name, url in servers.items():
            uptime, status = check_status(name, url)
            ranking.append({
                "group": group,
                "name": name,
                "url": url,
                "uptime_horas": uptime,
                "status": status
            })

    top5 = sorted(ranking, key=lambda x: x["uptime_horas"], reverse=True)[:5]

    html = """
    <html>
    <head>
    <title>Monitor de DNS - Uptime</title>
    <style>
    body { font-family: Arial; background-color: #121212; color: #ffffff; text-align: center; }
    table { width: 80%%; margin: auto; border-collapse: collapse; }
    th, td { border: 1px solid #444; padding: 10px; }
    th { background-color: #333; }
    h1 { color: #4CAF50; }
    </style>
    </head>
    <body>
    <h1>📊 TOP 5 Servidores por Uptime</h1>
    <table>
    <tr><th>Servidor</th><th>Grupo</th><th>Uptime (h)</th><th>Status</th></tr>
    """
    for server in top5:
        html += f"<tr><td>{server['name']}</td><td>{server['group']}</td><td>{server['uptime_horas']}</td><td>{server['status']}</td></tr>"

    html += "</table></body></html>"
    return Markup(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
