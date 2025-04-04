
import requests
from flask import Flask, render_template_string
import socket

app = Flask(__name__)

SERVIDORES = [
    ("Ztcentral", "ZEUS", "http://ztcentral.top:80"),
    ("AplusHM", "ZEUS", "http://aplushm.top"),
    ("Strmg", "ZEUS", "http://strmg.top"),
    ("Newxczs", "ZEUS", "http://newxczs.top"),
    ("AFS4Zer", "CLUB", "http://afs4zer.vip:80"),
    ("Ztuni", "UNIPLAY", "http://ztuni.top:80"),
    ("Testezeiro", "UNIPLAY", "http://testezeiro.com:80"),
    ("Techon", "POWERPLAY", "http://techon.one:80"),
    ("Tuptu1", "P2CINE", "https://tuptu1.live"),
    ("Tyuo22", "P2CINE", "https://tyuo22.club"),
    ("AB22", "P2CINE", "https://ab22.store"),
    ("Tojole", "LIVE21", "http://tojole.net:80"),
    ("BXPLux", "BXPLAY", "http://bxplux.top:80"),
    ("BandNews", "ELITE", "http://bandnews.asia:80"),
    ("CDN Trek", "BLAZE", "http://cdntrek.xyz:80"),
    ("Natkcz", "BLAZE", "http://natkcz.xyz:80"),
]

def verificar_servidor(url):
    try:
        host = url.replace("http://", "").replace("https://", "").split("/")[0]
        ip = socket.gethostbyname(host)
        s = socket.create_connection((ip, 80), timeout=6)
        s.close()
        return True
    except:
        return False

@app.route("/")
def index():
    status_list = []
    for nome, grupo, url in SERVIDORES:
        online = verificar_servidor(url)
        status_list.append((nome, grupo, "🟢" if online else "🔴"))

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <title>Status dos Servidores DNS</title>
    </head>
    <body>
        <h2>🔍 Todos os Servidores DNS</h2>
        <table border='1' cellpadding='6'>
            <tr><th>Servidor</th><th>Grupo</th><th>Status</th></tr>
            {% for nome, grupo, status in status_list %}
            <tr>
                <td>{{nome}}</td>
                <td>{{grupo}}</td>
                <td style='text-align:center;'>{{status}}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, status_list=status_list)

if __name__ == "__main__":
    app.run(debug=True)
