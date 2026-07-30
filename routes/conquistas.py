from flask import Blueprint, render_template, session

from models import medalha as medalha_model
from utils.helpers import login_obrigatorio

bp = Blueprint("conquistas", __name__)


@bp.route("/conquistas")
@login_obrigatorio
def index():
    todas = medalha_model.listar_todas()
    conquistadas = medalha_model.listar_conquistadas(session["usuario_id"])
    codigos_conquistados = {m["codigo"] for m in conquistadas}

    return render_template(
        "conquistas.html",
        todas=todas,
        codigos_conquistados=codigos_conquistados,
        conquistadas=conquistadas,
    )
