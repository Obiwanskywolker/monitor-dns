
from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# Lista de servidores e seus grupos
servidores = {
    "Ztcentral": ("ZEUS", "http://ztcentral.top:80"),
    "AplusHM": ("ZEUS", "http://aplushm.top"),
    "Strmg": ("ZEUS", "http://strmg.top"),
    "Newxczs": ("ZEUS", "http://newxczs.top"),
    "AFS4Zer": ("CLUB", "http://afs4zer.vip:80"),
    "Ztuni": ("UNIPLAY", "http://ztuni.top:80"),
    "Testezeiro": ("UNIPLAY", "http://testezeiro.com:80"),
    "Techon": ("POWERPLAY", "http://techon.one:80"),
    "Tuptu1": ("P2CINE", "https://tuptu1.live"),
    "Tyuo22": ("P2CINE", "https://tyuo22.club"),
    "AB22": ("P2CINE", "https://ab22.store"),
    "Tojole": ("LIVE21", "http://tojole.net:80"),
    "BXPLux": ("BXPLAY", "http://bxplux.top:80"),
    "BandNews": ("ELITE", "http://bandnews.asia:80"),
    "CDN Trek": ("BLAZE", "http://cdntrek.xyz:80"),
    "Natkcz": ("BLAZE", "http://natkcz.xyz:80")
}

def check_status(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        if 200 <= response.status_code < 400:
            return "🟢"
        else:
            return "🔴"
    except:
        return "🔴"

@app.route("/")
def index():
    status_servidores = []
    for nome, (grupo, url) in servidores.items():
        status = check_status(url)
        status_servidores.append((nome, grupo, status))

    html = """
    <html><head><meta charset='utf-8'>
    <style>
        body { font-family: Arial; background: #fff; padding: 20px; }
        h2 { color: #333; }
        table { width: 300px; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #000; padding: 8px; text-align: left; }
        th { background: #f0f0f0; }
    </style>
    </head><body>
    <h2>🔍 Todos os Servidores DNS</h2>
    <table>
        <tr><th>Servidor</th><th>Grupo</th><th>Status</th></tr>
        {% for s in servidores %}
            <tr><td>{{s[0]}}</td><td>{{s[1]}}</td><td>{{s[2]}}</td></tr>
        {% endfor %}
    </table>
    </body></html>
    """
    return render_template_string(html, servidores=status_servidores)

if __name__ == "__main__":
    app.run(debug=True)
