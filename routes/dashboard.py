from flask import Blueprint, render_template, session

from models import usuario as usuario_model
from utils.helpers import login_obrigatorio

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_obrigatorio
def index():
    user = usuario_model.buscar_por_id(session["usuario_id"])
    return render_template("dashboard.html", user=user)
