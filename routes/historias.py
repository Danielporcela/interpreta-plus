from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from models import usuario as usuario_model
from services import historia_service, progresso_service, conquista_service, ia_service
from utils.helpers import login_obrigatorio

bp = Blueprint("historias", __name__)


@bp.route("/treino")
@login_obrigatorio
def treino():
    user = usuario_model.buscar_por_id(session["usuario_id"])
    hist, perguntas = historia_service.obter_proxima_atividade(user["id"], user["nivel"])

    if hist is None:
        flash("Você concluiu todas as histórias disponíveis neste nível por enquanto!")
        return redirect(url_for("dashboard.index"))

    return render_template("historia.html", historia=hist, perguntas=perguntas)


@bp.route("/treino/responder", methods=["POST"])
@login_obrigatorio
def responder():
    user = usuario_model.buscar_por_id(session["usuario_id"])
    historia_id = int(request.form["historia_id"])

    from models import pergunta as pergunta_model

    perguntas = pergunta_model.listar_por_historia(historia_id)

    respostas_usuario = {
        chave.replace("pergunta_", ""): valor
        for chave, valor in request.form.items()
        if chave.startswith("pergunta_")
    }

    acertos, erros, detalhes = historia_service.corrigir_respostas(perguntas, respostas_usuario)
    pontuacao = historia_service.calcular_pontuacao(acertos, len(perguntas))

    from models import resposta as resposta_model

    for p in perguntas:
        escolha = respostas_usuario.get(str(p["id"]))
        if escolha is not None:
            resposta_model.registrar(user["id"], p["id"], escolha, escolha == p["correta"])

    novo_nivel = progresso_service.salvar_resultado(
        user["id"], historia_id, user["nivel"], acertos, erros, pontuacao
    )

    usuario_atualizado = usuario_model.buscar_por_id(user["id"])
    novas_medalhas = conquista_service.verificar_e_conceder(
        usuario_atualizado, acertos, erros, len(perguntas)
    )

    feedback_ia = ia_service.gerar_feedback(pontuacao, acertos, erros)

    return render_template(
        "resultado.html",
        acertos=acertos,
        erros=erros,
        pontuacao=pontuacao,
        detalhes=detalhes,
        subiu_nivel=novo_nivel != user["nivel"],
        novo_nivel=novo_nivel,
        novas_medalhas=novas_medalhas,
        feedback_ia=feedback_ia,
    )
