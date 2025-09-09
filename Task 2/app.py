import os
import sqlite3
from flask import Flask, request, redirect, render_template, jsonify

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "courses.db")

app = Flask(__name__, template_folder="templates")

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            duration TEXT,
            mode TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, duration, mode, description FROM courses")
    rows = cur.fetchall()
    conn.close()
    return render_template("index.html", courses=[
        {"id": r[0], "title": r[1], "duration": r[2], "mode": r[3], "description": r[4]}
        for r in rows
    ])

# Add new course
@app.route("/course", methods=["POST"])
def add_course():
    title = request.form.get("title")
    duration = request.form.get("duration")
    mode = request.form.get("mode")
    desc = request.form.get("description")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO courses (title, duration, mode, description) VALUES (?, ?, ?, ?)",
                (title, duration, mode, desc))
    conn.commit()
    conn.close()
    return redirect("/")

# Edit course
@app.route("/course/<int:course_id>/edit", methods=["POST"])
def edit_course(course_id):
    title = request.form.get("title")
    duration = request.form.get("duration")
    mode = request.form.get("mode")
    desc = request.form.get("description")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE courses SET title=?, duration=?, mode=?, description=? WHERE id=?",
                (title, duration, mode, desc, course_id))
    conn.commit()
    conn.close()
    return redirect("/")

# Delete course
@app.route("/course/<int:course_id>/delete", methods=["POST"])
def delete_course(course_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM courses WHERE id=?", (course_id,))
    conn.commit()
    conn.close()
    return redirect("/")

# Local description generator
@app.route("/api/generate_description", methods=["POST"])
def generate_description():
    data = request.get_json()
    title = data.get("title", "Untitled Course")
    duration = data.get("duration", "some weeks")
    mode = data.get("mode", "online")

    # Simple filler description
    desc = f"{title} is a {duration} {mode} program designed to help learners improve their skills."
    return jsonify({"description": desc})

if __name__ == "__main__":
    app.run(debug=True, port=5002)
