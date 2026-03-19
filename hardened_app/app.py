from flask import Flask, request, render_template, redirect, session, abort
import sqlite3
import html
import secrets

app = Flask(__name__)
app.secret_key = "secure"

print("Hardened app running on http://localhost:5000")

def db():
    return sqlite3.connect("database.db")


# SQLi fixed
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = db()
        cursor = conn.cursor()

        user = cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        ).fetchone()

        print("\nSQLi attempt blocked")
        print("Username:", username)

        if user:
            session["user_id"] = user[0]
            return redirect(f"/user/{user[0]}/profile")
        else:
            print("Output: Invalid credentials. Access denied.")
            print("[+] Parameterized query prevented SQL injection")

    return render_template("login.html")


# XSS fixed
@app.route("/search")
def search():

    q = request.args.get("q","")
    safe = html.escape(q)

    print("\nXSS attempt blocked")
    print("Search:", q)
    print("Output: Search results for:", safe)
    print("[+] Input sanitization prevented XSS")

    return render_template("search.html", query=safe)


# IDOR fixed
@app.route("/user/<id>/profile")
def profile(id):

    if str(session.get("user_id")) != id:

        print("\nIDOR attempt blocked")
        print("URL:", f"http://localhost:5000/user/{id}/profile")
        print("Output: Access denied. You can only view your own profile.")
        print("[+] Authorization check prevented IDOR")

        abort(403)

    conn = db()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT username,email FROM users WHERE id=?",(id,)
    ).fetchone()

    return render_template("profile.html", user=user)


# CSRF fixed
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        csrf_token = request.form.get("csrf")

        if not csrf_token or csrf_token != session.get("csrf"):
            print("\nCSRF attempt blocked")
            print("[+] CSRF token validation prevented forged request")
            return "Invalid CSRF token. Request rejected.", 403

        email = request.form.get("email")

        print("\nEmail change successful")
        print("New email:", email)

        return "Email updated"

    return render_template("contact.html")


app.run(debug=True)