from models.db import get_db


def listar_por_nivel(nivel):
    db = get_db()
    return db.execute(
        "SELECT * FROM historias WHERE nivel = ? ORDER BY id", (nivel,)
    ).fetchall()


def listar_todas():
    db = get_db()
    return db.execute("SELECT * FROM historias ORDER BY nivel, id").fetchall()


def buscar_por_id(historia_id):
    db = get_db()
    return db.execute("SELECT * FROM historias WHERE id = ?", (historia_id,)).fetchone()


def proxima_nao_feita(usuario_id, nivel):
    """Retorna a próxima história do nível que o usuário ainda não completou."""
    db = get_db()
    return db.execute(
        """SELECT h.* FROM historias h
           WHERE h.nivel = ?
             AND h.id NOT IN (
                 SELECT historia_id FROM progresso WHERE usuario_id = ?
             )
           ORDER BY h.id LIMIT 1""",
        (nivel, usuario_id),
    ).fetchone()


def criar(titulo, texto, nivel, categoria):
    db = get_db()
    cur = db.execute(
        "INSERT INTO historias (titulo, texto, nivel, categoria) VALUES (?, ?, ?, ?)",
        (titulo, texto, nivel, categoria),
    )
    db.commit()
    return cur.lastrowid


def atualizar(historia_id, titulo, texto, nivel, categoria):
    db = get_db()
    db.execute(
        "UPDATE historias SET titulo = ?, texto = ?, nivel = ?, categoria = ? WHERE id = ?",
        (titulo, texto, nivel, categoria, historia_id),
    )
    db.commit()


def excluir(historia_id):
    db = get_db()
    db.execute("DELETE FROM perguntas WHERE historia_id = ?", (historia_id,))
    db.execute("DELETE FROM historias WHERE id = ?", (historia_id,))
    db.commit()
