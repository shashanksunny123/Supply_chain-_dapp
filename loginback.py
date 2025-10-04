from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    db_reg_no = request.form.get("regno")
    password = request.form.get("password")

    conn = sqlite3.connect("users2.db")
    c = conn.cursor()
    c.execute("SELECT name, regno, password FROM users2 WHERE regno=? AND password=?", (db_reg_no,password))
    user = c.fetchone()
    conn.close()

    if not user:
        return jsonify({"success": False, "message": "User not found!"})

    db_name, db_reg_no, db_password = user

    if password == db_password:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "name": db_name,
            "regno": db_reg_no
        })
    else:
        return jsonify({"success": False, "message": "Invalid password!"})
