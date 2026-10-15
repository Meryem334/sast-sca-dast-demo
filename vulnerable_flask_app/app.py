import os
import subprocess
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]  # secret lu dans l'environnement

ALLOWED = {"date": ["date"], "uptime": ["uptime"]}  # liste blanche de commandes


@app.after_request
def security_headers(resp):
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; frame-ancestors 'none'; form-action 'self'"
    )
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    return resp


@app.route('/hello')
def hello():
    name = request.args.get('name', 'Guest')
    return f"<h1>Hello Page</h1><p>Hello, {escape(name)}!</p>"


@app.route('/execute')
def execute():
    key = request.args.get('cmd', 'date')
    if key not in ALLOWED:
        return "Commande non autorisée", 400
    out = subprocess.run(ALLOWED[key], capture_output=True, text=True)  # pas de shell=True
    return f"<pre>{escape(out.stdout)}</pre>"


# /admin supprimé

if __name__ == '__main__':
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(debug=debug, host='0.0.0.0')
