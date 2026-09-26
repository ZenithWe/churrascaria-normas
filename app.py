from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instance" / "normas.db"

BUSINESS = {
    "name": "Churrascaria Norma's",
    "tagline": "Comida brasileira, churrasco e pizza no coração de Nova Lima.",
    "phone": "+55 31 3541-3001",
    "phone_display": "(31) 3541-3001",
    "address": "R. José d'Ávila, 40 - Centro, Nova Lima - MG, 34000-000",
    "lat": -19.9829356,
    "lng": -43.8517134,
    "rating": "4,5",
    "reviews": "2,3 mil+",
    "ifood_url": "https://www.ifood.com.br/delivery/nova-lima-mg/normas-restaurante-centro/68f610ab-01e0-4ffc-a795-35e23ae35411",
    "instagram_url": "https://www.instagram.com/normasrestaurante/",
    "maps_url": "https://www.google.com/maps/search/?api=1&query=Churrascaria+Norma%27s+Nova+Lima",
    "waze_url": "https://www.waze.com/ul?q=Churrascaria%20Norma%27s%20Nova%20Lima&navigate=yes",
}

HOURS = [
    ("Segunda", "11:00–15:00"),
    ("Terça", "11:00–15:00 · 17:00–22:00"),
    ("Quarta", "11:00–15:00 · 17:00–23:00"),
    ("Quinta", "11:00–15:00 · 17:00–23:00"),
    ("Sexta", "11:00–15:00 · 17:00–01:00"),
    ("Sábado", "11:00–15:00"),
    ("Domingo", "11:00–22:00"),
]

FEATURED = [
    {
        "name": "Self-service com churrasco",
        "desc": "Almoço com variedade de comida brasileira e opções de carnes.",
        "icon": "🔥",
    },
    {
        "name": "Filé ao gorgonzola",
        "desc": "Um dos pratos citados com frequência nas avaliações públicas.",
        "icon": "🥩",
    },
    {
        "name": "Isca de tilápia",
        "desc": "Opção muito mencionada por clientes do restaurante.",
        "icon": "🐟",
    },
    {
        "name": "Pizzas",
        "desc": "Pizzaria e churrascaria reunidas no mesmo endereço.",
        "icon": "🍕",
    },
]

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY", "dev-change-this-secret"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                people INTEGER NOT NULL,
                notes TEXT,
                status TEXT NOT NULL DEFAULT 'Pendente',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


@app.context_processor
def globals_for_templates():
    return {"business": BUSINESS, "hours": HOURS}


@app.route("/")
def index():
    return render_template("index.html", featured=FEATURED)


@app.post("/reservar")
def reserve():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    date = request.form.get("date", "").strip()
    time = request.form.get("time", "").strip()
    notes = request.form.get("notes", "").strip()

    try:
        people = int(request.form.get("people", "0"))
    except ValueError:
        people = 0

    if not all([name, phone, date, time]) or people < 1 or people > 30:
        flash("Confira os dados da reserva e tente novamente.", "error")
        return redirect(url_for("index", _anchor="reservas"))

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO reservations (name, phone, date, time, people, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (name, phone, date, time, people, notes, datetime.now().isoformat(timespec="seconds")),
        )

    flash("Pedido de reserva enviado. O restaurante deve confirmar a disponibilidade.", "success")
    return redirect(url_for("index", _anchor="reservas"))


@app.post("/contato")
def contact():
    name = request.form.get("name", "").strip()
    contact_value = request.form.get("contact", "").strip()
    message = request.form.get("message", "").strip()

    if not all([name, contact_value, message]):
        flash("Preencha os campos de contato.", "error")
        return redirect(url_for("index", _anchor="contato"))

    with get_db() as conn:
        conn.execute(
            "INSERT INTO contacts (name, contact, message, created_at) VALUES (?, ?, ?, ?)",
            (name, contact_value, message, datetime.now().isoformat(timespec="seconds")),
        )

    flash("Mensagem recebida.", "success")
    return redirect(url_for("index", _anchor="contato"))


@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        expected = os.getenv("ADMIN_PASSWORD", "troque-esta-senha")
        if password == expected:
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("Senha inválida.", "error")
    return render_template("login.html")


@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/admin")
@admin_required
def admin():
    with get_db() as conn:
        reservations = conn.execute(
            "SELECT * FROM reservations ORDER BY date ASC, time ASC, id DESC"
        ).fetchall()
        contacts = conn.execute(
            "SELECT * FROM contacts ORDER BY id DESC LIMIT 100"
        ).fetchall()
    return render_template("admin.html", reservations=reservations, contacts=contacts)


@app.post("/admin/reservas/<int:reservation_id>/status")
@admin_required
def reservation_status(reservation_id: int):
    status = request.form.get("status", "Pendente")
    if status not in {"Pendente", "Confirmada", "Cancelada"}:
        status = "Pendente"
    with get_db() as conn:
        conn.execute("UPDATE reservations SET status = ? WHERE id = ?", (status, reservation_id))
    return redirect(url_for("admin"))


@app.get("/health")
def health():
    return {"status": "ok", "service": "normas-site"}


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG") == "1")
