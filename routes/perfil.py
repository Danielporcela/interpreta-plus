from flask import Blueprint, render_template, session

from models import usuario as usuario_model
from models import progresso as progresso_model
from utils.helpers import login_obrigatorio

bp = Blueprint("perfil", __name__)


@bp.route("/perfil")
@login_obrigatorio
def index():
    user = usuario_model.buscar_por_id(session["usuario_id"])
    historico = progresso_model.listar_por_usuario(user["id"])
    return render_template("perfil.html", user=user, historico=historico)
