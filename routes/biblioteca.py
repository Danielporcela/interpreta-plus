from flask import Blueprint, render_template, redirect, url_for, flash, session

from models import biblioteca as biblioteca_model
from models import historia as historia_model
from models import pergunta as pergunta_model
from utils.helpers import login_obrigatorio

bp = Blueprint("biblioteca", __name__)


@bp.route("/biblioteca")
@login_obrigatorio
def index():
    todas = biblioteca_model.listar_todas()
    concluidas = biblioteca_model.ids_concluidas(session["usuario_id"])

    por_nivel = {}
    for h in todas:
        por_nivel.setdefault(h["nivel"], []).append(h)

    return render_template(
        "biblioteca.html", por_nivel=por_nivel, concluidas=concluidas
    )


@bp.route("/biblioteca/historia/<int:historia_id>")
@login_obrigatorio
def praticar(historia_id):
    hist = historia_model.buscar_por_id(historia_id)
    if hist is None:
        flash("História não encontrada.")
        return redirect(url_for("biblioteca.index"))

    perguntas = pergunta_model.listar_por_historia(historia_id)
    return render_template("historia.html", historia=hist, perguntas=perguntas)
