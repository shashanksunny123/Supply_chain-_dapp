from flask import Flask, request, jsonify, render_template
import sqlite3, random, string

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect('users2.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users3 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    dob TEXT NOT NULL,
                    father_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    reg_num TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

def generate_user_id():
    return str(random.randint(10000000, 99999999))

def generate_password(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

# Routes
@app.route("/")
def home():
    return render_template("signin.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    dob = request.form.get("dob")
    father_name = request.form.get("father_name") 
    phone = request.form.get("phone") 
    email = request.form.get("email")

    conn = sqlite3.connect("users2.db")
    c = conn.cursor() 
    c.execute("SELECT * FROM users3 WHERE email=?" ,(email,))
    existing_user = c.fetchone()

    if existing_user:
        conn.close()
        return jsonify({"success":False,"message": "❌ User already exists with this email!"})

    reg_num = generate_user_id()
    password = generate_password()

    c.execute("""INSERT INTO users3
                 (name, dob, father_name, phone, email, reg_num, password)
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
              (name, dob, father_name, phone, email, reg_num, password))

    conn.commit()
    conn.close()

    return jsonify({
        "success":True,
        "message": "✅ Registration successful!",
        "reg_num":reg_num,
        "email": email,
        "password": password
    })

@app.route("/login", methods=["POST"])
def login():
    db_reg_num = request.form.get("regno")
    password = request.form.get("password")

    conn = sqlite3.connect("users2.db")
    c = conn.cursor()
    c.execute("SELECT name, reg_num, password FROM users3 WHERE reg_num=? AND password=?", (db_reg_num, password))
    user = c.fetchone()
    conn.close()

    if not user:
        return jsonify({"success": False, "message": "User not found!"})

    db_name, db_reg_num, password = user
    return jsonify({"success": True, "message": "Login successful",
                    "name": db_name, "user_id": db_reg_num})

if __name__ == "__main__":
    app.run(debug=True)
