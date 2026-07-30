from models.db import get_db


def registrar(usuario_id, historia_id, nivel, pontos, acertos, erros):
    db = get_db()
    db.execute(
        """INSERT INTO progresso (usuario_id, historia_id, nivel, pontos, acertos, erros)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (usuario_id, historia_id, nivel, pontos, acertos, erros),
    )
    db.commit()


def listar_por_usuario(usuario_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM progresso WHERE usuario_id = ? ORDER BY data DESC",
        (usuario_id,),
    ).fetchall()


def contar_historias_concluidas(usuario_id):
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as total FROM progresso WHERE usuario_id = ?",
        (usuario_id,),
    ).fetchone()
    return row["total"]
