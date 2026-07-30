"""
Cria as tabelas (se não existirem) e popula o banco com histórias e medalhas de exemplo.
Executar a partir da raiz do projeto: python database/seed.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.db import get_db, init_db

app = create_app()


def seed():
    with app.app_context():
        init_db(app)
        db = get_db()

        seed_historias(db)
        seed_medalhas(db)
        seed_admin(db)


def seed_admin(db):
    from werkzeug.security import generate_password_hash

    ja_tem = db.execute(
        "SELECT 1 FROM usuarios WHERE email = ?", ("admin@interpreta.com",)
    ).fetchone()
    if ja_tem:
        print("Conta de administrador já existe.")
        return

    db.execute(
        """INSERT INTO usuarios (nome, email, senha, tipo, is_admin)
           VALUES (?, ?, ?, ?, ?)""",
        ("Administrador", "admin@interpreta.com", generate_password_hash("admin123"), "responsavel", 1),
    )
    db.commit()
    print("Conta de administrador criada: admin@interpreta.com / admin123")


def seed_historias(db):
    ja_tem = db.execute("SELECT COUNT(*) as total FROM historias").fetchone()["total"]
    if ja_tem > 0:
        print("Histórias já cadastradas, seed não é necessário.")
        return

    caminho = os.path.join(os.path.dirname(__file__), "..", "data", "historias.json")
    with open(caminho, "r", encoding="utf-8") as f:
        historias = json.load(f)

    for h in historias:
        cur = db.execute(
            "INSERT INTO historias (titulo, texto, nivel, categoria) VALUES (?, ?, ?, ?)",
            (h["titulo"], h["texto"], h["nivel"], h["categoria"]),
        )
        historia_id = cur.lastrowid

        for p in h["perguntas"]:
            db.execute(
                """INSERT INTO perguntas
                   (historia_id, texto, a, b, c, d, e, correta, explicacao)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    historia_id,
                    p["texto"],
                    p["a"],
                    p["b"],
                    p["c"],
                    p["d"],
                    p.get("e", ""),
                    p["correta"],
                    p.get("explicacao", ""),
                ),
            )

    db.commit()
    print(f"{len(historias)} histórias cadastradas com sucesso!")


def seed_medalhas(db):
    ja_tem = db.execute("SELECT COUNT(*) as total FROM medalhas").fetchone()["total"]
    if ja_tem > 0:
        print("Medalhas já cadastradas, seed não é necessário.")
        return

    caminho = os.path.join(os.path.dirname(__file__), "..", "data", "medalhas.json")
    with open(caminho, "r", encoding="utf-8") as f:
        medalhas = json.load(f)

    for m in medalhas:
        db.execute(
            "INSERT INTO medalhas (codigo, titulo, descricao, icone) VALUES (?, ?, ?, ?)",
            (m["codigo"], m["titulo"], m["descricao"], m["icone"]),
        )
    db.commit()
    print(f"{len(medalhas)} medalhas cadastradas com sucesso!")


if __name__ == "__main__":
    seed()
