from models.db import get_db


def listar_por_historia(historia_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM perguntas WHERE historia_id = ? ORDER BY id", (historia_id,)
    ).fetchall()


def buscar_por_id(pergunta_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM perguntas WHERE id = ?", (pergunta_id,)
    ).fetchone()


def criar(historia_id, texto, a, b, c, d, e, correta, explicacao):
    db = get_db()
    cur = db.execute(
        """INSERT INTO perguntas (historia_id, texto, a, b, c, d, e, correta, explicacao)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (historia_id, texto, a, b, c, d, e, correta, explicacao),
    )
    db.commit()
    return cur.lastrowid


def atualizar(pergunta_id, texto, a, b, c, d, e, correta, explicacao):
    db = get_db()
    db.execute(
        """UPDATE perguntas
           SET texto = ?, a = ?, b = ?, c = ?, d = ?, e = ?, correta = ?, explicacao = ?
           WHERE id = ?""",
        (texto, a, b, c, d, e, correta, explicacao, pergunta_id),
    )
    db.commit()


def excluir(pergunta_id):
    db = get_db()
    db.execute("DELETE FROM perguntas WHERE id = ?", (pergunta_id,))
    db.commit()
