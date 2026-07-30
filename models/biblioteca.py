from models.db import get_db


def listar_todas():
    db = get_db()
    return db.execute("SELECT * FROM historias ORDER BY nivel, id").fetchall()


def ids_concluidas(usuario_id):
    db = get_db()
    linhas = db.execute(
        "SELECT DISTINCT historia_id FROM progresso WHERE usuario_id = ?", (usuario_id,)
    ).fetchall()
    return {l["historia_id"] for l in linhas}
