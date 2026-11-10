# INTENTIONALLY VULNERABLE - for secure code review practice only. Do not deploy.
import hashlib
import os
import pickle
import sqlite3
import subprocess
from flask import Flask, request, render_template_string, send_file

app = Flask(__name__)
app.secret_key = "dev123"  # intentionally insecure training example
DB = "users.db"

def db():
    return sqlite3.connect(DB)

@app.route("/init")
def init():
    c = db()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, password TEXT, is_admin INT)")
    c.execute("INSERT INTO users(name,password,is_admin) VALUES('admin',?,1)",
              (hashlib.md5(b"admin").hexdigest(),))
    c.commit()
    return "ok"

@app.route("/login", methods=["POST"])
def login():
    u, p = request.form["user"], request.form["pw"]
    q = f"SELECT * FROM users WHERE name='{u}' AND password='{hashlib.md5(p.encode()).hexdigest()}'"
    return "welcome" if db().execute(q).fetchone() else "denied"

@app.route("/hello")
def hello():
    return render_template_string("<h1>Hello " + request.args.get("name", "") + "</h1>")

@app.route("/ping")
def ping():
    return subprocess.check_output("ping -c 1 " + request.args["host"], shell=True)

@app.route("/download")
def download():
    return send_file(os.path.join("uploads", request.args["f"]))

@app.route("/load", methods=["POST"])
def load():
    return str(pickle.loads(request.data))

@app.route("/user/<int:uid>")
def user(uid):
    return str(db().execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
