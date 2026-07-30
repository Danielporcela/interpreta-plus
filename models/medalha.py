from models.db import get_db


def listar_todas():
    db = get_db()
    return db.execute("SELECT * FROM medalhas ORDER BY id").fetchall()


def buscar_por_codigo(codigo):
    db = get_db()
    return db.execute("SELECT * FROM medalhas WHERE codigo = ?", (codigo,)).fetchone()


def listar_conquistadas(usuario_id):
    db = get_db()
    return db.execute(
        """SELECT m.*, um.data_conquista
           FROM medalhas m
           JOIN usuario_medalhas um ON um.medalha_id = m.id
           WHERE um.usuario_id = ?
           ORDER BY um.data_conquista DESC""",
        (usuario_id,),
    ).fetchall()


def usuario_ja_tem(usuario_id, medalha_id):
    db = get_db()
    row = db.execute(
        "SELECT 1 FROM usuario_medalhas WHERE usuario_id = ? AND medalha_id = ?",
        (usuario_id, medalha_id),
    ).fetchone()
    return row is not None


def conceder(usuario_id, codigo):
    """Concede a medalha ao usuário, se ele ainda não tiver. Retorna a medalha se for nova."""
    medalha = buscar_por_codigo(codigo)
    if medalha is None:
        return None
    if usuario_ja_tem(usuario_id, medalha["id"]):
        return None

    db = get_db()
    db.execute(
        "INSERT INTO usuario_medalhas (usuario_id, medalha_id) VALUES (?, ?)",
        (usuario_id, medalha["id"]),
    )
    db.commit()
    return medalha
