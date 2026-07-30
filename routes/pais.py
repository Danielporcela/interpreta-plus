from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from models import usuario as usuario_model
from models import vinculo as vinculo_model
from services import relatorio_service
from utils.helpers import login_obrigatorio

bp = Blueprint("pais", __name__)


@bp.route("/pais")
@login_obrigatorio
def index():
    user = usuario_model.buscar_por_id(session["usuario_id"])

    if user["tipo"] != "responsavel":
        flash("Esta área é exclusiva para contas de responsável.")
        return redirect(url_for("dashboard.index"))

    criancas = vinculo_model.listar_criancas(user["id"])
    return render_template("pais.html", criancas=criancas)


@bp.route("/pais/vincular", methods=["POST"])
@login_obrigatorio
def vincular():
    user = usuario_model.buscar_por_id(session["usuario_id"])
    if user["tipo"] != "responsavel":
        flash("Esta área é exclusiva para contas de responsável.")
        return redirect(url_for("dashboard.index"))

    email_crianca = request.form.get("email_crianca", "").strip().lower()
    crianca = usuario_model.buscar_por_email(email_crianca)

    if crianca is None:
        flash("Não encontramos nenhuma conta de criança com esse e-mail.")
    elif crianca["tipo"] != "crianca":
        flash("Esse e-mail não pertence a uma conta de criança.")
    else:
        criado = vinculo_model.criar_vinculo(user["id"], crianca["id"])
        if criado:
            flash(f"{crianca['nome']} foi vinculado(a) à sua conta com sucesso.")
        else:
            flash("Essa criança já está vinculada à sua conta.")

    return redirect(url_for("pais.index"))


@bp.route("/pais/crianca/<int:crianca_id>")
@login_obrigatorio
def detalhe(crianca_id):
    user = usuario_model.buscar_por_id(session["usuario_id"])
    if user["tipo"] != "responsavel" or not vinculo_model.responsavel_pode_ver(user["id"], crianca_id):
        flash("Você não tem acesso a essa conta.")
        return redirect(url_for("pais.index"))

    crianca = usuario_model.buscar_por_id(crianca_id)
    resumo = relatorio_service.resumo_geral(crianca_id)
    por_categoria = relatorio_service.desempenho_por_categoria(crianca_id)

    return render_template(
        "pais_detalhe.html", crianca=crianca, resumo=resumo, por_categoria=por_categoria
    )
