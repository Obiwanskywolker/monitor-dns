
from flask import Flask, render_template_string
import requests

app = Flask(__name__)

SERVIDORES = [
    {"nome": "Ztcentral", "grupo": "ZEUS", "url": "http://ztcentral.top:80"},
    {"nome": "AplusHM", "grupo": "ZEUS", "url": "http://aplushm.top"},
    {"nome": "Strmg", "grupo": "ZEUS", "url": "http://strmg.top"},
    {"nome": "Newxczs", "grupo": "ZEUS", "url": "http://newxczs.top"},
    {"nome": "AFS4Zer", "grupo": "CLUB", "url": "http://afs4zer.vip:80"},
    {"nome": "Ztuni", "grupo": "UNIPLAY", "url": "http://ztuni.top:80"},
    {"nome": "Testezeiro", "grupo": "UNIPLAY", "url": "http://testezeiro.com:80"},
    {"nome": "Techon", "grupo": "POWERPLAY", "url": "http://techon.one:80"},
    {"nome": "Tuptu1", "grupo": "P2CINE", "url": "https://tuptu1.live"},
    {"nome": "Tyuo22", "grupo": "P2CINE", "url": "https://tyuo22.club"},
    {"nome": "AB22", "grupo": "P2CINE", "url": "https://ab22.store"},
    {"nome": "Tojole", "grupo": "LIVE21", "url": "http://tojole.net:80"},
    {"nome": "BXPLux", "grupo": "BXPLAY", "url": "http://bxplux.top:80"},
    {"nome": "BandNews", "grupo": "ELITE", "url": "http://bandnews.asia:80"},
    {"nome": "CDN Trek", "grupo": "BLAZE", "url": "http://cdntrek.xyz:80"},
    {"nome": "Natkcz", "grupo": "BLAZE", "url": "http://natkcz.xyz:80"},
]

@app.route("/")
def index():
    resultados = []
    for s in SERVIDORES:
        try:
            response = requests.head(s["url"], timeout=10, allow_redirects=True)
            status_code = response.status_code
            status = "🟢" if 200 <= status_code < 400 else "🔴"
        except Exception as e:
            status = "🔴"
        resultados.append({
            "nome": s["nome"],
            "grupo": s["grupo"],
            "url": s["url"],
            "status": status
        })

    html = '''
    <html><head><title>Status DNS</title></head><body>
    <h2>🧪 Todos os Servidores DNS</h2>
    <table border="1" cellpadding="8"><tr><th>Servidor</th><th>Grupo</th><th>Status</th></tr>
    {% for r in resultados %}
    <tr><td>{{ r.nome }}</td><td>{{ r.grupo }}</td><td>{{ r.status }}</td></tr>
    {% endfor %}
    </table></body></html>
    '''
    return render_template_string(html, resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)
