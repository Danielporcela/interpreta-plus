from models import usuario as usuario_model
from models import progresso as progresso_model

HISTORIAS_POR_NIVEL = 2  # quantas histórias completas para subir de nível (MVP)


def salvar_resultado(usuario_id, historia_id, nivel_atual, acertos, erros, pontuacao):
    progresso_model.registrar(usuario_id, historia_id, nivel_atual, pontuacao, acertos, erros)
    usuario_model.atualizar_pontos(usuario_id, pontuacao)
    usuario_model.registrar_atividade_do_dia(usuario_id)

    total_concluidas = progresso_model.contar_historias_concluidas(usuario_id)
    novo_nivel = (total_concluidas // HISTORIAS_POR_NIVEL) + 1
    if novo_nivel != nivel_atual:
        usuario_model.atualizar_nivel(usuario_id, novo_nivel)

    return novo_nivel
