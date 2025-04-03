import requests
import time
import socket
from urllib.parse import urlparse
from flask import Flask, jsonify, send_from_directory, request, redirect, render_template_string, url_for

app = Flask(__name__)

# ... (resto do dicionário "servers" e "status_data" igual ao anterior)

# Funções auxiliares mantidas...

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        action = request.form.get('action')
        group = request.form['group']
        name = request.form['name']

        if action == 'delete':
            if group in servers:
                servers[group] = [dns for dns in servers[group] if dns['name'] != name]
                status_data[group].pop(name, None)
        elif action == 'edit':
            url = request.form['url']
            for dns in servers[group]:
                if dns['name'] == name:
                    dns['url'] = url
                    status_data[group][name]['url'] = url
        elif action == 'add':
            url = request.form['url']
            if group in servers:
                servers[group].append({"name": name, "url": url})
            else:
                servers[group] = [{"name": name, "url": url}]
            status_data.setdefault(group, {})[name] = {
                "url": url, "status": "Desconhecido", "uptime": 100.0, "failures": 0, "last_check": "-"
            }
        return redirect('/admin')

    html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Painel Admin</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .status-online { color: green; font-weight: bold; }
            .status-offline { color: red; font-weight: bold; }
            .status-desconhecido { color: gray; font-weight: bold; }
        </style>
    </head>
    <body class="p-4">
    <div class="container">
        <h2 class="mb-4">Painel Administrador</h2>
        <form method="post" class="mb-5 row g-3">
            <input type="hidden" name="action" value="add">
            <div class="col-md-4">
                <label class="form-label">Grupo</label>
                <input name="group" class="form-control">
            </div>
            <div class="col-md-4">
                <label class="form-label">Nome da DNS</label>
                <input name="name" class="form-control">
            </div>
            <div class="col-md-4">
                <label class="form-label">URL</label>
                <input name="url" class="form-control">
            </div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">Adicionar DNS</button>
            </div>
        </form>

        <h3>DNS Registradas</h3>
        {% for group, dns_list in status_data.items() %}
            <div class="mt-4">
                <h4>{{ group }}</h4>
                <ul class="list-group">
                {% for name, data in dns_list.items() %}
                    {% set status_class = 'status-' + data['status'].lower() %}
                    <li class="list-group-item">
                        <strong>{{ name }}</strong> - {{ data['url'] }}<br>
                        Status:
                        {% if data['status'] == 'Online' %}🟢{% elif data['status'] == 'Offline' %}🔴{% else %}⚪{% endif %}
                        <span class="{{ status_class }}">{{ data['status'] }}</span>
                        | Uptime:
                        <div class="progress" style="height: 20px; max-width: 300px; display:inline-block; vertical-align: middle;">
                            <div class="progress-bar" role="progressbar" style="width: {{ data['uptime'] }}%;" aria-valuenow="{{ data['uptime'] }}" aria-valuemin="0" aria-valuemax="100">{{ data['uptime'] }}%</div>
                        </div>
                        <form method="post" style="display:inline">
                            <input type="hidden" name="action" value="delete">
                            <input type="hidden" name="group" value="{{ group }}">
                            <input type="hidden" name="name" value="{{ name }}">
                            <button class="btn btn-danger btn-sm">Remover</button>
                        </form>
                        <form method="post" class="d-inline">
                            <input type="hidden" name="action" value="edit">
                            <input type="hidden" name="group" value="{{ group }}">
                            <input type="hidden" name="name" value="{{ name }}">
                            <input type="text" name="url" value="{{ data['url'] }}" class="form-control d-inline-block" style="width: 300px;">
                            <button class="btn btn-warning btn-sm">Atualizar URL</button>
                        </form>
                    </li>
                {% endfor %}
                </ul>
            </div>
        {% endfor %}
        <br><a href="/" class="btn btn-secondary mt-4">← Voltar para o painel</a>
    </div>
    </body>
    </html>
    '''
    return render_template_string(html, status_data=status_data)

if __name__ == '__main__':
    import threading
    thread = threading.Thread(target=check_dns, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
