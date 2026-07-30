from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models import usuario as usuario_model

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        user = usuario_model.buscar_por_email(email)
        if user and check_password_hash(user["senha"], senha):
            session["usuario_id"] = user["id"]
            session["nome"] = user["nome"]
            session["tipo"] = user["tipo"]
            session["is_admin"] = bool(user["is_admin"])
            if user["is_admin"]:
                return redirect(url_for("admin.index"))
            if user["tipo"] == "responsavel":
                return redirect(url_for("pais.index"))
            return redirect(url_for("dashboard.index"))

        flash("E-mail ou senha inválidos.")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        idade = request.form.get("idade", "")
        tipo = request.form.get("tipo", "crianca")
        if tipo not in ("crianca", "responsavel"):
            tipo = "crianca"

        if not nome or not email or not senha:
            flash("Preencha todos os campos.")
            return redirect(url_for("auth.cadastro"))

        if usuario_model.buscar_por_email(email):
            flash("Este e-mail já está cadastrado.")
            return redirect(url_for("auth.cadastro"))

        senha_hash = generate_password_hash(senha)
        idade_int = int(idade) if idade.isdigit() else None
        usuario_id = usuario_model.criar_usuario(nome, email, senha_hash, idade_int, tipo)

        session["usuario_id"] = usuario_id
        session["nome"] = nome
        session["tipo"] = tipo
        session["is_admin"] = False
        if tipo == "responsavel":
            return redirect(url_for("pais.index"))
        return redirect(url_for("dashboard.index"))

    return render_template("cadastro.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
