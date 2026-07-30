from models import medalha as medalha_model
from models import progresso as progresso_model


def verificar_e_conceder(usuario_atualizado, acertos, erros, total_perguntas):
    """
    Verifica as regras simples de conquista e concede as medalhas novas.
    Retorna a lista de medalhas conquistadas AGORA (para exibir na tela de resultado).
    """
    novas = []

    total_concluidas = progresso_model.contar_historias_concluidas(usuario_atualizado["id"])

    regras = []

    if total_concluidas >= 1:
        regras.append("primeiro_dia")

    if usuario_atualizado["sequencia"] >= 3:
        regras.append("sequencia_3")

    if usuario_atualizado["sequencia"] >= 7:
        regras.append("sequencia_7")

    if usuario_atualizado["pontos"] >= 100:
        regras.append("pontuacao_100")

    if usuario_atualizado["nivel"] >= 2:
        regras.append("nivel_2")

    if erros == 0 and total_perguntas > 0:
        regras.append("gabarito")

    for codigo in regras:
        conquistada = medalha_model.conceder(usuario_atualizado["id"], codigo)
        if conquistada is not None:
            novas.append(conquistada)

    return novas
