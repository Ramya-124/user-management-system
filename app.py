from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
import webbrowser
import threading

app = Flask(__name__)
app.secret_key = "secret123"


def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        try:
            valid = validate_email(email)
            email = valid.email

        except EmailNotValidError as e:
            flash(str(e), "warning")
            return redirect("/signup")

        if not name:
            flash("Name is required", "warning")
            return redirect("/signup")

        if len(password) < 8:
            flash("Password must be at least 8 characters", "warning")
            return redirect("/signup")

        if not any(char.isupper() for char in password):
            flash(
                "Password must contain at least one uppercase letter",
                "warning"
            )
            return redirect("/signup")

        if not any(char.isdigit() for char in password):
            flash(
                "Password must contain at least one number",
                "warning"
            )
            return redirect("/signup")

        if password != confirm_password:
            flash("Passwords do not match", "warning")
            return redirect("/signup")

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE LOWER(email)=?",
            (email,)
        )

        existing_user = cur.fetchone()

        if existing_user:
            conn.close()
            flash("Email already registered", "warning")
            return redirect("/signup")

        hashed_password = generate_password_hash(password)

        cur.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, hashed_password)
        )

        conn.commit()
        conn.close()

        flash(
            "Registration Successful. Please Login.",
            "success"
        )

        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE LOWER(email)=?",
            (email,)
        )

        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):

            session["user_id"] = user[0]
            session["name"] = user[1]
            session["email"] = user[2]

            flash("Login Successful", "success")
            return redirect("/profile")

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


@app.route("/users")
def users():

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT id, name, email FROM users")

    data = cur.fetchall()

    conn.close()

    return str(data)


@app.route("/profile")
def profile():

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    return render_template(
        "profile.html",
        name=session["name"],
        email=session["email"]
    )


@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged Out Successfully",
        "success"
    )

    return redirect("/login")


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False)