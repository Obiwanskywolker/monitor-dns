
import requests
import time
import socket
from urllib.parse import urlparse
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

servers = {'ZEUS': [{'name': 'Ztcentral', 'url': 'http://ztcentral.top:80'}, {'name': 'AplusHM', 'url': 'http://aplushm.top'}, {'name': 'Strmg', 'url': 'http://strmg.top'}, {'name': 'Newxczs', 'url': 'http://newxczs.top'}], 'CLUB': [{'name': 'AFS4Zer', 'url': 'http://afs4zer.vip:80'}], 'UNIPLAY': [{'name': 'Ztuni', 'url': 'http://ztuni.top:80'}, {'name': 'Testezeiro', 'url': 'http://testezeiro.com:80'}], 'POWERPLAY': [{'name': 'Techon', 'url': 'http://techon.one:80'}], 'P2CINE': [{'name': 'Tuptu1', 'url': 'http://tuptu1.xyz:80'}], 'LIVE21': [{'name': 'Tojole', 'url': 'http://tojole.net:80'}], 'ELITE': [{'name': 'BandNews', 'url': 'http://bandnews.asia:80'}], 'BXPLAY': [{'name': 'BXPLux', 'url': 'http://bxplux.top:80'}], 'CDN Trek': [{'name': 'CDN Trek', 'url': 'http://cdntrk.xyz:80'}, {'name': 'Natkcz', 'url': 'http://natkcz.xyz:80'}]}

status_data = {}
for group, dns_list in servers.items():
    status_data[group] = {}
    for dns in dns_list:
        status_data[group][dns['name']] = {
            "url": dns['url'],
            "status": "Desconhecido",
            "uptime": 100.0,
            "failures": 0,
            "last_check": "-"
        }

def is_port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except:
        return False

def check_dns_loop(once=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    print("🔎 Iniciando verificação de DNS...")

    for group, dns_list in servers.items():
        for dns in dns_list:
            name = dns['name']
            url = dns['url']
            try:
                response = requests.get(url, timeout=10, allow_redirects=True, headers=headers)
                if response.status_code == 200:
                    status_data[group][name]['status'] = 'Online'
                    print(f"✅ {name} ({group}): Online")
                else:
                    raise Exception("Código diferente de 200")
            except:
                parsed = urlparse(url)
                host = parsed.hostname
                port = parsed.port or (443 if parsed.scheme == 'https' else 80)
                if is_port_open(host, port):
                    status_data[group][name]['status'] = 'Online'
                    print(f"⚠️ {name} ({group}): Online (porta aberta, sem resposta HTTP)")
                else:
                    status_data[group][name]['status'] = 'Offline'
                    status_data[group][name]['failures'] += 1
                    print(f"❌ {name} ({group}): Offline")

            total_checks = status_data[group][name]['failures'] + 1
            if total_checks > 0:
                uptime = ((total_checks - status_data[group][name]['failures']) / total_checks) * 100
                status_data[group][name]['uptime'] = round(uptime, 1)
            else:
                status_data[group][name]['uptime'] = 100.0

            status_data[group][name]['last_check'] = time.strftime('%H:%M')

    if not once:
        time.sleep(300)
        check_dns_loop()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/status')
def get_status():
    ranking = []
    for group in status_data:
        for name, info in status_data[group].items():
            ranking.append({"name": name, "uptime": info['uptime'], "group": group})
    top5 = sorted(ranking, key=lambda x: x['uptime'], reverse=True)[:5]
    return jsonify({"status": status_data, "top5": top5})

if __name__ == '__main__':
    import threading
    # Roda verificação contínua em thread
    check_thread = threading.Thread(target=check_dns_loop, daemon=True)
    check_thread.start()

    # Roda verificação inicial direta (sem esperar 5 min)
    check_dns_loop(once=True)

    app.run(host='0.0.0.0', port=5000)
