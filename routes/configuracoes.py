from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

from models import configuracao as configuracao_model
from models import usuario as usuario_model
from models.db import get_db
from utils.helpers import login_obrigatorio

bp = Blueprint("configuracoes", __name__)


@bp.route("/configuracoes", methods=["GET", "POST"])
@login_obrigatorio
def index():
    usuario_id = session["usuario_id"]

    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "preferencias":
            som_ativado = 1 if request.form.get("som_ativado") else 0
            animacoes_ativadas = 1 if request.form.get("animacoes_ativadas") else 0
            lembrete_diario = 1 if request.form.get("lembrete_diario") else 0
            configuracao_model.atualizar(usuario_id, som_ativado, animacoes_ativadas, lembrete_diario)
            flash("Preferências salvas com sucesso.")

        elif acao == "senha":
            senha_atual = request.form.get("senha_atual", "")
            nova_senha = request.form.get("nova_senha", "")
            user = usuario_model.buscar_por_id(usuario_id)

            if not check_password_hash(user["senha"], senha_atual):
                flash("Senha atual incorreta.")
            elif len(nova_senha) < 4:
                flash("A nova senha deve ter pelo menos 4 caracteres.")
            else:
                db = get_db()
                db.execute(
                    "UPDATE usuarios SET senha = ? WHERE id = ?",
                    (generate_password_hash(nova_senha), usuario_id),
                )
                db.commit()
                flash("Senha alterada com sucesso.")

        return redirect(url_for("configuracoes.index"))

    config = configuracao_model.obter(usuario_id)
    return render_template("configuracoes.html", config=config)
