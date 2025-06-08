from flask import Flask, request, render_template, session, jsonify
from urllib.parse import urlparse
import socket
import ipaddress
import requests
import os

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
BLACKLIST = {'localhost',
    '127.0.0.1',
    '::1',
    '192.168.0.0/16',
    '0.0.0.0/8',
    '192.0.0.0/24',
    '192.0.2.0/24',
    '198.18.0.0/15',
    '198.51.100.0/24',
    }

def add_colba_to_session(colba):
    session[colba] = True
    order = session.get("inventory_order", [])
    if colba not in order:
        order.append(colba)
        session["inventory_order"] = order

@app.route('/', methods=['GET', 'POST'])
def index():
    mah_id = None
    cold = session.get("cold", False)
    if request.method == "POST":
        url = request.form['url']
        parser = urlparse(url).hostname
        info = socket.gethostbyname(parser)
        global_check = ipaddress.ip_address(info).is_global
        if parser not in BLACKLIST and global_check == True:
            resp = requests.get(url, timeout=(1, 3), allow_redirects=False)
            text = resp.text.strip()
            if text == "ALGO_OK":
                add_colba_to_session("algo")
                mah_id = {"type": "success", "text": "Вы взяли колбу из альгоцеха!"}
            elif text == "HOT_OK":
                add_colba_to_session("hot")
                mah_id = {"type": "success", "text": "Вы получили колбу из горячего цеха!"}
            elif text == "PESTICIDE_OK":
                add_colba_to_session("pesticide")
                mah_id = {"type": "success", "text": "Вы вытащили колбу из пестицидного цеха!"}
            elif text == "COLD_OK":
                add_colba_to_session("cold")
                mah_id = {"type": "success", "text": "Вы достали колбу из холодного цеха!"}
            elif text == "Access denied!":
                mah_id = {"type": "error", "text": "Access denied!"}
            else:
                mah_id = {"type": "info", "text": text}
            return render_template('index.html', mah_id=mah_id, cold=session.get("cold", False))
        elif global_check == False:
            mah_id = {"type": "error", "text": "Access Violation: Private IP Detected"}
            return render_template('index.html', mah_id=mah_id, cold=cold)
    return render_template('index.html', cold=cold)

@app.route('/get_inventory')
def get_inventory():
    return jsonify({
        "algo": session.get("algo", False),
        "pesticide": session.get("pesticide", False),
        "hot": session.get("hot", False),
        "cold": session.get("cold", False),
        "order": session.get("inventory_order", [])
    })

@app.route('/get_flag')
def get_flag():
    if all(session.get(k) for k in ['algo', 'pesticide', 'hot', 'cold']):
        with open('flag') as f:
            return f.read().strip()
    return "Флаг не выдан. Соберите все колбы.", 403

@app.route('/algo')
def algo_colba():
    add_colba_to_session("algo")
    return "ALGO_OK"

@app.route('/hot')
def hot_colba():
    add_colba_to_session("hot")
    return "HOT_OK"

@app.route('/pesticide')
def pesticide_colba():
    add_colba_to_session("pesticide")
    return "PESTICIDE_OK"

@app.route('/cold')
def cold_colba():
    if request.remote_addr not in ("127.0.0.1", "::1"):
        return "Access denied!"
    add_colba_to_session("cold")
    return "COLD_OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=False)
