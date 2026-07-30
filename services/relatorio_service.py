from models.db import get_db


def resumo_geral(crianca_id):
    db = get_db()
    row = db.execute(
        """SELECT
               COUNT(*) as total_respostas,
               SUM(acertou) as total_acertos
           FROM respostas WHERE usuario_id = ?""",
        (crianca_id,),
    ).fetchone()

    total = row["total_respostas"] or 0
    acertos = row["total_acertos"] or 0
    percentual = round((acertos / total) * 100) if total > 0 else 0

    return {"total_respostas": total, "total_acertos": acertos, "percentual_acertos": percentual}


def desempenho_por_categoria(crianca_id):
    """Agrupa o percentual de acertos pela categoria da história (proxy de habilidade)."""
    db = get_db()
    linhas = db.execute(
        """SELECT h.categoria as categoria,
                  COUNT(*) as total,
                  SUM(r.acertou) as acertos
           FROM respostas r
           JOIN perguntas p ON p.id = r.pergunta_id
           JOIN historias h ON h.id = p.historia_id
           WHERE r.usuario_id = ?
           GROUP BY h.categoria
           ORDER BY h.categoria""",
        (crianca_id,),
    ).fetchall()

    resultado = []
    for l in linhas:
        percentual = round((l["acertos"] / l["total"]) * 100) if l["total"] > 0 else 0
        resultado.append(
            {"categoria": l["categoria"], "total": l["total"], "acertos": l["acertos"], "percentual": percentual}
        )
    return resultado
