from models.db import get_db


PADRAO = {"som_ativado": 1, "animacoes_ativadas": 1, "lembrete_diario": 1}


def obter(usuario_id):
    db = get_db()
    row = db.execute(
        "SELECT * FROM configuracoes WHERE usuario_id = ?", (usuario_id,)
    ).fetchone()

    if row is None:
        db.execute(
            """INSERT INTO configuracoes (usuario_id, som_ativado, animacoes_ativadas, lembrete_diario)
               VALUES (?, ?, ?, ?)""",
            (usuario_id, PADRAO["som_ativado"], PADRAO["animacoes_ativadas"], PADRAO["lembrete_diario"]),
        )
        db.commit()
        row = db.execute(
            "SELECT * FROM configuracoes WHERE usuario_id = ?", (usuario_id,)
        ).fetchone()

    return row


def atualizar(usuario_id, som_ativado, animacoes_ativadas, lembrete_diario):
    db = get_db()
    obter(usuario_id)  # garante que a linha existe
    db.execute(
        """UPDATE configuracoes
           SET som_ativado = ?, animacoes_ativadas = ?, lembrete_diario = ?
           WHERE usuario_id = ?""",
        (int(som_ativado), int(animacoes_ativadas), int(lembrete_diario), usuario_id),
    )
    db.commit()
