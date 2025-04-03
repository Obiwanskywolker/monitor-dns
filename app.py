
from flask import Flask, render_template_string
import requests

app = Flask(__name__)

SERVIDORES = [
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def verificar_status(url):
    try:
        response = requests.head(url, headers=HEADERS, timeout=5)
        if response.status_code < 400:
            return True
        else:
            response = requests.get(url, headers=HEADERS, timeout=5, stream=True)
            return response.status_code < 400
    except:
        return False

@app.route("/")
def index():
    status = []
    for grupo, nome, url in SERVIDORES:
        online = verificar_status(url)
        status.append({
            "grupo": grupo,
            "nome": nome,
            "status": "🟢" if online else "🔴"
        })

    html = """
    <html>
    <head>
        <title>Todos os Servidores DNS</title>
    </head>
    <body style="background:#fff;font-family:Arial">
        <h2>🔍 Todos os Servidores DNS</h2>
        <table border="1" cellspacing="0" cellpadding="5">
            <tr><th>Servidor</th><th>Grupo</th><th>Status</th></tr>
            {% for s in status %}
            <tr>
                <td>{{s.nome}}</td>
                <td>{{s.grupo}}</td>
                <td style="text-align:center;">{{s.status}}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, status=status)

if __name__ == '__main__':
    app.run(debug=True)
