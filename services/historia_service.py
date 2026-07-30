from models import historia, pergunta


def obter_proxima_atividade(usuario_id, nivel):
    """Escolhe a próxima história do nível atual do usuário."""
    hist = historia.proxima_nao_feita(usuario_id, nivel)
    if hist is None:
        return None, []
    perguntas = pergunta.listar_por_historia(hist["id"])
    return hist, perguntas


def corrigir_respostas(perguntas, respostas_usuario):
    """
    perguntas: lista de rows do banco
    respostas_usuario: dict {pergunta_id (str): alternativa escolhida (a/b/c/d/e)}
    Retorna: acertos, erros, detalhes (lista de dicts para exibir no resultado)
    """
    acertos = 0
    erros = 0
    detalhes = []

    for p in perguntas:
        escolha = respostas_usuario.get(str(p["id"]))
        correta = escolha is not None and escolha == p["correta"]
        if correta:
            acertos += 1
        else:
            erros += 1
        detalhes.append(
            {
                "pergunta": p["texto"],
                "escolha": escolha,
                "correta_letra": p["correta"],
                "correta": correta,
                "explicacao": p["explicacao"],
            }
        )

    return acertos, erros, detalhes


def calcular_pontuacao(acertos, total):
    if total == 0:
        return 0
    return round((acertos / total) * 100)
