
from flask import Flask, render_template_string, redirect
import requests
import json
import os
import time

app = Flask(__name__)

# Lista de servidores organizados por grupo
servidores = [
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
    ("BLAZE", "Natkcz", "http://natkcz.xyz:80")
]

DATA_FILE = "data/uptime.json"

# Carrega dados existentes
def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except Exception as e:
                print("Erro ao carregar JSON:", e)
                return {}
    return {}

# Salva dados atualizados
def salvar_dados(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Verifica status dos servidores
def verificar_servidores():
    data = carregar_dados()
    for grupo, nome, url in servidores:
        try:
            resposta = requests.get(url, timeout=5)
            online = resposta.status_code == 200
        except:
            online = False

        if nome not in data:
            data[nome] = {"uptime": 0, "status": False, "group": grupo}

        if online:
            tempo_passado = 5 * 60  # 5 minutos
            data[nome]["uptime"] += tempo_passado
            data[nome]["status"] = True
        else:
            data[nome]["status"] = False

        print(f"[DEBUG] {nome} - {'ONLINE' if online else 'OFFLINE'} - Uptime: {data[nome]['uptime']}s")

    salvar_dados(data)

@app.route("/atualizar")
def atualizar():
    verificar_servidores()
    return redirect("/")

@app.route("/")
def index():
    data = carregar_dados()
    ranking = [
        {
            "name": nome,
            "group": info["group"],
            "uptime_horas": round(info["uptime"] / 3600, 2),
            "status": info["status"]
        }
        for nome, info in data.items()
    ]
    ranking.sort(key=lambda x: x["uptime_horas"], reverse=True)

    html = """
    <html><head><title>Todos os Servidores</title></head><body>
    <h1>📊 Todos os Servidores</h1>
    <table border=1 cellpadding=6 cellspacing=0>
    <tr><th>Servidor</th><th>Grupo</th><th>Uptime (horas)</th><th>Status</th></tr>
    {% for item in ranking %}
      <tr>
        <td>{{ item.name }}</td>
        <td>{{ item.group }}</td>
        <td>{{ item.uptime_horas }}</td>
        <td>{{ "🟢" if item.status else "🔴" }}</td>
      </tr>
    {% endfor %}
    </table>
    <p><i>Atualizado a cada 5 minutos. Acesse /atualizar manualmente para testar.</i></p>
    </body></html>
    """
    return render_template_string(html, ranking=ranking)

if __name__ == "__main__":
    app.run(debug=True)
