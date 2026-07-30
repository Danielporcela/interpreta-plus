from flask import Blueprint, render_template, request, redirect, url_for, flash

from models import historia as historia_model
from models import pergunta as pergunta_model
from utils.helpers import admin_obrigatorio

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
@admin_obrigatorio
def index():
    historias = historia_model.listar_todas()
    return render_template("admin_historias.html", historias=historias)


@bp.route("/historia/nova", methods=["GET", "POST"])
@admin_obrigatorio
def nova_historia():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        texto = request.form.get("texto", "").strip()
        nivel = int(request.form.get("nivel", 1))
        categoria = request.form.get("categoria", "geral").strip()

        if not titulo or not texto:
            flash("Preencha título e texto da história.")
            return redirect(url_for("admin.nova_historia"))

        historia_id = historia_model.criar(titulo, texto, nivel, categoria)
        flash("História cadastrada. Agora adicione as perguntas.")
        return redirect(url_for("admin.editar_historia", historia_id=historia_id))

    return render_template("admin_historia_form.html", historia=None, perguntas=[])


@bp.route("/historia/<int:historia_id>/editar", methods=["GET", "POST"])
@admin_obrigatorio
def editar_historia(historia_id):
    historia = historia_model.buscar_por_id(historia_id)
    if historia is None:
        flash("História não encontrada.")
        return redirect(url_for("admin.index"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        texto = request.form.get("texto", "").strip()
        nivel = int(request.form.get("nivel", 1))
        categoria = request.form.get("categoria", "geral").strip()
        historia_model.atualizar(historia_id, titulo, texto, nivel, categoria)
        flash("História atualizada com sucesso.")
        return redirect(url_for("admin.editar_historia", historia_id=historia_id))

    perguntas = pergunta_model.listar_por_historia(historia_id)
    return render_template("admin_historia_form.html", historia=historia, perguntas=perguntas)


@bp.route("/historia/<int:historia_id>/excluir", methods=["POST"])
@admin_obrigatorio
def excluir_historia(historia_id):
    historia_model.excluir(historia_id)
    flash("História excluída.")
    return redirect(url_for("admin.index"))


@bp.route("/historia/<int:historia_id>/pergunta/nova", methods=["POST"])
@admin_obrigatorio
def nova_pergunta(historia_id):
    dados = request.form
    pergunta_model.criar(
        historia_id,
        dados.get("texto", "").strip(),
        dados.get("a", "").strip(),
        dados.get("b", "").strip(),
        dados.get("c", "").strip(),
        dados.get("d", "").strip(),
        dados.get("e", "").strip(),
        dados.get("correta", "a").strip(),
        dados.get("explicacao", "").strip(),
    )
    flash("Pergunta adicionada.")
    return redirect(url_for("admin.editar_historia", historia_id=historia_id))


@bp.route("/pergunta/<int:pergunta_id>/excluir", methods=["POST"])
@admin_obrigatorio
def excluir_pergunta(pergunta_id):
    pergunta = pergunta_model.buscar_por_id(pergunta_id)
    if pergunta is None:
        flash("Pergunta não encontrada.")
        return redirect(url_for("admin.index"))

    historia_id = pergunta["historia_id"]
    pergunta_model.excluir(pergunta_id)
    flash("Pergunta excluída.")
    return redirect(url_for("admin.editar_historia", historia_id=historia_id))
