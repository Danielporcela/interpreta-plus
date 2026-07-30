from models.db import get_db


def criar_usuario(nome, email, senha_hash, idade, tipo="crianca"):
    db = get_db()
    cur = db.execute(
        "INSERT INTO usuarios (nome, email, senha, idade, tipo) VALUES (?, ?, ?, ?, ?)",
        (nome, email, senha_hash, idade, tipo),
    )
    db.commit()
    return cur.lastrowid


def buscar_por_email(email):
    db = get_db()
    return db.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()


def buscar_por_id(usuario_id):
    db = get_db()
    return db.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()


def atualizar_pontos(usuario_id, pontos_ganhos):
    db = get_db()
    db.execute(
        "UPDATE usuarios SET pontos = pontos + ? WHERE id = ?",
        (pontos_ganhos, usuario_id),
    )
    db.commit()


def atualizar_nivel(usuario_id, novo_nivel):
    db = get_db()
    db.execute("UPDATE usuarios SET nivel = ? WHERE id = ?", (novo_nivel, usuario_id))
    db.commit()


def registrar_atividade_do_dia(usuario_id):
    """Atualiza dias de estudo e sequência com base na data da última atividade."""
    from datetime import date

    db = get_db()
    usuario = buscar_por_id(usuario_id)
    hoje = date.today().isoformat()

    if usuario["ultima_atividade"] == hoje:
        return  # já contabilizado hoje

    if usuario["ultima_atividade"]:
        ultima = date.fromisoformat(usuario["ultima_atividade"])
        diferenca = (date.today() - ultima).days
        nova_sequencia = usuario["sequencia"] + 1 if diferenca == 1 else 1
    else:
        nova_sequencia = 1

    db.execute(
        """UPDATE usuarios
           SET dias_estudo = dias_estudo + 1,
               sequencia = ?,
               ultima_atividade = ?
           WHERE id = ?""",
        (nova_sequencia, hoje, usuario_id),
    )
    db.commit()
