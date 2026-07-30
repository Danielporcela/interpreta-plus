from models.db import get_db


def registrar(usuario_id, pergunta_id, resposta, acertou):
    db = get_db()
    db.execute(
        """INSERT INTO respostas (usuario_id, pergunta_id, resposta, acertou)
           VALUES (?, ?, ?, ?)""",
        (usuario_id, pergunta_id, resposta, int(acertou)),
    )
    db.commit()
