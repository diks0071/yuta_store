from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import json, os, datetime

app = Flask(__name__)
app.secret_key = "yuta_store_secret"

ADMIN_USER = "admin"
ADMIN_PASS = generate_password_hash("Sandi123321")

def load_json(file):
    with open(file) as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return render_template("index.html", products=load_json("data.json"))

@app.route("/order", methods=["POST"])
def order():
    orders = load_json("orders.json")
    orders.append({
        "product": request.form["product"],
        "price": request.form["price"],
        "user": request.form["user"],
        "time": datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    })
    save_json("orders.json", orders)
    return redirect("/")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["user"] == ADMIN_USER and \
           check_password_hash(ADMIN_PASS, request.form["pass"]):
            session["admin"] = True
            return redirect("/admin")
    return render_template("login.html")

@app.route("/admin", methods=["GET","POST"])
def admin():
    if not session.get("admin"):
        return redirect("/login")

    data = load_json("data.json")
    if request.method == "POST":
        for i in range(len(data)):
            data[i]["price"] = request.form[f"price{i}"]
        save_json("data.json", data)

    return render_template("admin.html", products=data)

@app.route("/orders")
def orders():
    if not session.get("admin"):
        return redirect("/login")
    return render_template("orders.html", orders=load_json("orders.json"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

