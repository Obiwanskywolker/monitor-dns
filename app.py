import requests
import time
import socket
from urllib.parse import urlparse
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

servers = {
    "ZEUS": [
        {"name": "Ztcentral", "url": "http://ztcentral.top:80"},
        {"name": "AplusHM", "url": "http://aplushm.top"},
        {"name": "Strmg", "url": "http://strmg.top"},
        {"name": "Newxczs", "url": "http://newxczs.top"}
    ],
    "CLUB": [{"name": "AFS4Zer", "url": "http://afs4zer.vip:80"}],
    "UNIPLAY": [
        {"name": "Ztuni", "url": "http://ztuni.top:80"},
        {"name": "Testezeiro", "url": "http://testezeiro.com:80"}
    ],
    "POWERPLAY": [{"name": "Techon", "url": "http://techon.one:80"}],
    "P2CINE": [
        {"name": "Tuptu1", "url": "https://tuptu1.live"},
        {"name": "Tyuo22", "url": "https://tyuo22.club"},
        {"name": "AB22", "url": "https://ab22.store"}
    ],
    "LIVE21": [{"name": "Tojole", "url": "http://tojole.net:80"}],
    "BXPLAY": [{"name": "BXPLux", "url": "http://bxplux.top:80"}],
    "ELITE": [{"name": "BandNews", "url": "http://bandnews.asia:80"}],
    "BLAZE": [
        {"name": "CDN Trek", "url": "http://cdntrek.xyz:80"},
        {"name": "Natkcz", "url": "http://natkcz.xyz:80"}
    ]
}

status_data = {}
for group, dns_list in servers.items():
    status_data[group] = {}
    for dns in dns_list:
        status_data[group][dns['name']] = {
            "url": dns['url'], "status": "Desconhecido", "uptime": 100.0,
            "failures": 0, "last_check": "-", "uptime_days": 0
        }

def is_port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except:
        return False

def check_dns():
    headers = {'User-Agent': 'Mozilla/5.0'}
    while True:
        print("Iniciando verificação de DNS...")
        for group, dns_list in servers.items():
            for dns in dns_list:
                name, url = dns['name'], dns['url']
                print(f"Verificando {name} - {url}")
                try:
                    response = requests.get(url, timeout=10, allow_redirects=True, headers=headers)
                    online = response.status_code == 200
                except Exception as e:
                    parsed = urlparse(url)
                    host, port = parsed.hostname, parsed.port or (443 if parsed.scheme == 'https' else 80)
                    print(f"Falha na requisição HTTP. Testando porta: {host}:{port}")
                    online = is_port_open(host, port)

                status_data[group][name]['status'] = 'Online' if online else 'Offline'
                if not online:
                    status_data[group][name]['failures'] += 1

                total_checks = status_data[group][name]['failures'] + 1
                uptime = ((total_checks - status_data[group][name]['failures']) / total_checks) * 100
                status_data[group][name]['uptime'] = round(uptime, 1)
                status_data[group][name]['uptime_days'] = round((uptime / 100) * (total_checks * 5) / 1440, 2)
                status_data[group][name]['last_check'] = time.strftime('%d/%m/%Y %H:%M')
        print("Verificação concluída. Aguardando próxima rodada...
")
        time.sleep(10)

@app.route('/')
def index():
    html_template = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Status dos DNS Monitorados</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f7f7f7; padding: 20px; }
            h2 { margin-top: 40px; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 40px; background: white; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
            th { background: #444; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            @media (max-width: 600px) {
                table, thead, tbody, th, td, tr { display: block; }
                td { border: none; border-bottom: 1px solid #eee; }
            }
        </style>
    </head>
    <body>
        <h1>Status dos DNS Monitorados</h1>
        {% for group, dns_list in status_data.items() %}
            <h2>{{ group }}</h2>
            <table>
                <thead>
                    <tr><th>Nome</th><th>Endereço</th><th>Status</th><th>Uptime</th><th>Uptime (dias)</th></tr>
                </thead>
                <tbody>
                    {% for name, info in dns_list.items() %}
                    <tr>
                        <td>{{ name }}</td>
                        <td><a href="{{ info.url }}" target="_blank">{{ info.url }}</a></td>
                        <td>{{ info.status }}</td>
                        <td>{{ info.uptime }}%</td>
                        <td>{{ info.uptime_days }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html_template, status_data=status_data)

@app.route('/api/status')
def get_status():
    ranking = [
        {"name": name, "uptime": info['uptime'], "uptime_days": info['uptime_days'], "group": group}
        for group, dns_list in status_data.items() for name, info in dns_list.items()
    ]
    top5 = sorted(ranking, key=lambda x: x['uptime'], reverse=True)[:5]
    return jsonify({"status": status_data, "top5": top5})

if __name__ == '__main__':
    import threading
    threading.Thread(target=check_dns, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
