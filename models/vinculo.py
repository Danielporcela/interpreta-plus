from models.db import get_db


def criar_vinculo(responsavel_id, crianca_id):
    db = get_db()
    ja_existe = db.execute(
        "SELECT 1 FROM vinculos WHERE responsavel_id = ? AND crianca_id = ?",
        (responsavel_id, crianca_id),
    ).fetchone()
    if ja_existe:
        return False

    db.execute(
        "INSERT INTO vinculos (responsavel_id, crianca_id) VALUES (?, ?)",
        (responsavel_id, crianca_id),
    )
    db.commit()
    return True


def listar_criancas(responsavel_id):
    db = get_db()
    return db.execute(
        """SELECT u.* FROM usuarios u
           JOIN vinculos v ON v.crianca_id = u.id
           WHERE v.responsavel_id = ?
           ORDER BY u.nome""",
        (responsavel_id,),
    ).fetchall()


def responsavel_pode_ver(responsavel_id, crianca_id):
    db = get_db()
    row = db.execute(
        "SELECT 1 FROM vinculos WHERE responsavel_id = ? AND crianca_id = ?",
        (responsavel_id, crianca_id),
    ).fetchone()
    return row is not None
