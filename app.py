import os
import datetime
import requests
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")

DNS_LIST = [
    {"name": "Tuptu1", "url": "http://tuptu1.xyz"},
    {"name": "Techon", "url": "http://techon.one"},
    {"name": "Testeezeiro", "url": "http://testeezeiro.com"},
    {"name": "Ztuni", "url": "http://ztuni.top:80"},
    {"name": "Aplushm", "url": "http://aplushm.top"},
    {"name": "Newxczs", "url": "http://newxczs.top"},
    {"name": "Strmg", "url": "http://strmg.top"},
    {"name": "Ztcentral", "url": "http://ztcentral.top"},
]

last_status = {}
last_checked = {}

def check_status(dns):
    try:
        response = requests.get(dns["url"], timeout=5)
        return response.status_code == 200
    except:
        return False

@app.route("/")
def index():
    status_list = []

    for dns in DNS_LIST:
        now = datetime.datetime.utcnow()
        name = dns["name"]
        url = dns["url"]

        online = check_status(dns)

        if name not in last_status:
            last_status[name] = online
            last_checked[name] = now
        elif online != last_status[name]:
            last_status[name] = online
            last_checked[name] = now

        delta = now - last_checked[name]
        uptime = f"{delta.days} dias"

        status_list.append({
            "name": name,
            "url": url,
            "status": "Online" if online else "Offline",
            "uptime": uptime
        })

    return render_template("index.html", status_list=status_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
