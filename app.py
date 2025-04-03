from flask import Flask, jsonify, render_template
import requests
import threading
import time
import os

app = Flask(__name__)

# Dados das DNS
DNS_LIST = [
    {"grupo": "BLAZE", "nome": "CDN Trek", "endereco": "http://cdntrek.xyz:80"},
    {"grupo": "BLAZE", "nome": "Natkcz", "endereco": "http://natkcz.xyz:80"},
    {"grupo": "BXPLAY", "nome": "BXPLux", "endereco": "http://bxplux.top:80"},
    {"grupo": "CLUB", "nome": "AFS4Zer", "endereco": "http://afs4zer.vip:80"},
    {"grupo": "ELITE", "nome": "BandNews", "endereco": "http://bandnews.asia:80"},
    {"grupo": "LIVE21", "nome": "Tojole", "endereco": "http://tojole.net:80"},
    {"grupo": "P2CINE", "nome": "Tuptu1", "endereco": "http://tuptu1.xyz:80"},
    {"grupo": "POWERPLAY", "nome": "Techon", "endereco": "http://techon.one:80"},
    {"grupo": "UNIPLAY", "nome": "Testezeiro", "endereco": "http://testezeiro.com:80"},
    {"grupo": "UNIPLAY", "nome": "Ztuni", "endereco": "http://ztuni.top:80"},
    {"grupo": "ZEUS", "nome": "AplusHM", "endereco": "http://aplushm.top:80"},
    {"grupo": "ZEUS", "nome": "Newxczs", "endereco": "http://newxczs.top:80"},
    {"grupo": "ZEUS", "nome": "Strmg", "endereco": "http://strmg.top:80"},
    {"grupo": "ZEUS", "nome": "Ztcentral", "endereco": "http://ztcentral.top:80"},
]

status_dns = {}

def verificar_dns():
    while True:
        for dns in DNS_LIST:
            try:
                response = requests.get(dns["endereco"], timeout=10)
                status_dns[dns["nome"]] = {"status": "Online", "codigo": response.status_code, "grupo": dns["grupo"]}
            except requests.RequestException:
                status_dns[dns["nome"]] = {"status": "Offline", "codigo": None, "grupo": dns["grupo"]}

        time.sleep(300)  # Verifica a cada 5 minutos

@app.route('/api/status')
def api_status():
    return jsonify(status_dns)

@app.route('/')
def index():
    return render_template('index.html', dns_list=DNS_LIST, status_dns=status_dns)

# Inicialização da thread de verificação
threading.Thread(target=verificar_dns, daemon=True).start()

# Configuração para Railway
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
