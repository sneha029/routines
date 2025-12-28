from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("todo.db")

def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT,
        user TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # TEMPORARY LOGIN (NO DB CHECK)
        session["user"] = username
        return redirect("/todo")

    return render_template("index.html")

@app.route("/todo", methods=["GET", "POST"])
def todo():
    if "user" not in session:
        return redirect("/")

    conn = get_db()

    if request.method == "POST":
        task = request.form["task"]
        conn.execute(
            "INSERT INTO tasks(task, user) VALUES (?, ?)",
            (task, session["user"])
        )
        conn.commit()

    tasks = conn.execute(
        "SELECT * FROM tasks WHERE user=?",
        (session["user"],)
    ).fetchall()

    print(tasks)   

    return render_template("todo.html",tasks=tasks)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)