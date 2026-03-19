from flask import Flask, request, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

print("Vulnerable app running on http://localhost:5000")

def db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return redirect("/login")


# LOGIN (SQLi)
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = db()
        cursor = conn.cursor()

        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        print("\nSQLi — Login page:")
        print("URL: http://localhost:5000/login")

        user = cursor.execute(query).fetchone()

        if user:

            print(f"Username: {username}")
            print(f"Password: {password}")
            print(f"Output: Welcome {user[1]}. Login successful.")

            if "'" in username or "--" in username:
                print("[!] SQL Injection successful — bypassed authentication")

            session["user_id"] = user[0]

            return redirect(f"/user/{user[0]}/profile")

    return render_template("login.html")


# SEARCH (XSS)
@app.route("/search")
def search():

    q = request.args.get("q","")

    print("\nXSS — Search page:")
    print("URL: http://localhost:5000/search")
    print("Search:", q)

    if "<script>" in q:
        print("Output: Script executes in browser")
        print("[!] XSS successful — malicious script ran in victim browser")
    else:
        print("Output: Search results for:", q)

    return render_template("search.html", query=q)


# PROFILE (IDOR)
@app.route("/user/<id>/profile")
def profile(id):

    conn = db()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT username,email FROM users WHERE id=?",(id,)
    ).fetchone()

    print("\nIDOR — Profile page")
    print("URL:", f"http://localhost:5000/user/{id}/profile")

    if user:

        print(f"Output: Welcome {user[0]}. Email: {user[1]}")

        if id != str(session.get("user_id")):
            print("[!] IDOR successful — accessed another user's private data")

    return render_template("profile.html", user=user)


# CSRF demo
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        print("\nCSRF — Settings form")

        # Check if user session exists
        user_id = session.get("user_id")

        if not user_id:
            print("[!] No authenticated user session found")
            print("[!] CSRF test triggered without login")
            return "User not logged in", 403

        email = request.form.get("email", "")

        conn = db()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET email=? WHERE id=?",
            (email, user_id)
        )

        conn.commit()

        print("[*] Sending forged request as victim...")
        print("[+] Victim's email changed to", email)
        print("[!] CSRF successful — action performed without victim's knowledge")

        return "Email updated!"

    return render_template("contact.html")

app.run(debug=True)