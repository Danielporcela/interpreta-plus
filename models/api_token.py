import secrets

from models.db import get_db


def gerar_token(usuario_id):
    """Cria um novo token de acesso para o usuário (usado pelo app móvel)."""
    db = get_db()
    token = secrets.token_hex(32)
    db.execute(
        "INSERT INTO api_tokens (usuario_id, token) VALUES (?, ?)",
        (usuario_id, token),
    )
    db.commit()
    return token


def buscar_usuario_id_por_token(token):
    if not token:
        return None
    db = get_db()
    row = db.execute(
        "SELECT usuario_id FROM api_tokens WHERE token = ?", (token,)
    ).fetchone()
    return row["usuario_id"] if row else None


def revogar_token(token):
    db = get_db()
    db.execute("DELETE FROM api_tokens WHERE token = ?", (token,))
    db.commit()
