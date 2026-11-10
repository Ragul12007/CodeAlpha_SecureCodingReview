import os
import re
import secrets
import sqlite3
import subprocess
from functools import wraps

from flask import Flask, request, session, abort, render_template_string, send_from_directory, jsonify
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")
DB = "users.db"
UPLOAD_DIR = os.path.abspath("uploads")
HOST_RE = re.compile(r"^[A-Za-z0-9.-]{1,253}$")

def db():
    return sqlite3.connect(DB)

def login_required(fn):
    @wraps(fn)
    def wrapper(*a, **k):
        if "uid" not in session:
            abort(401)
        return fn(*a, **k)
    return wrapper

def init_db():
    c = db()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT UNIQUE, password TEXT, is_admin INT)")
    pw = os.environ.get("ADMIN_PASSWORD")
    if pw:
        c.execute("INSERT OR IGNORE INTO users(name,password,is_admin) VALUES('admin',?,1)",
                  (generate_password_hash(pw),))
    c.commit()

@app.route("/login", methods=["POST"])
def login():
    row = db().execute("SELECT id,password FROM users WHERE name=?", (request.form.get("user", ""),)).fetchone()
    if row and check_password_hash(row[1], request.form.get("pw", "")):
        session["uid"] = row[0]
        return "welcome"
    return "denied", 401

@app.route("/hello")
def hello():
    return render_template_string("<h1>Hello {{ name }}</h1>", name=request.args.get("name", ""))

@app.route("/ping")
@login_required
def ping():
    host = request.args.get("host", "")
    if not HOST_RE.match(host):
        abort(400)
    out = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)
    return escape(out.stdout)

@app.route("/download")
@login_required
def download():
    return send_from_directory(UPLOAD_DIR, request.args.get("f", ""))

@app.route("/load", methods=["POST"])
@login_required
def load():
    data = request.get_json(silent=True)
    if data is None:
        abort(400)
    return jsonify(data)

@app.route("/user/<int:uid>")
@login_required
def user(uid):
    if uid != session["uid"]:
        abort(403)
    row = db().execute("SELECT id,name FROM users WHERE id=?", (uid,)).fetchone()
    return jsonify(row)

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="127.0.0.1")
